from typing import  Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import threading
import os
import time
import uuid
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
# Find .env file in ai2025 directory (parent of graph directory)
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

# Local imports (relative to graph package)
from .gen import gen_context, gen_mcq, MCQ
from .refine import refine_context, refine_mcqs as refine_mcqs_api, RefinedContext, RefinedMCQ
from .review import review_mcq, review_context, Review

# ============== LANGSMITH TRACING CONFIGURATION ==============

# Load from environment variables
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "mcq-generation")

def configure_langsmith(
    api_key: str = None, 
    project: str = None, 
    tracing: bool = True,
    endpoint: str = "https://api.smith.langchain.com"
):
    """
    Configure LangSmith tracing for the MCQ generation workflow.
    
    Args:
        api_key: LangSmith API key
        project: Project name in LangSmith dashboard
        tracing: Enable/disable tracing
        endpoint: LangSmith API endpoint
    
    View traces at: https://smith.langchain.com/
    """
    # Use provided api_key or fallback to environment variable
    final_api_key = api_key or os.getenv("LANGSMITH_API_KEY", "")
    final_project = project or os.getenv("LANGSMITH_PROJECT", "mcq-generation")
    
    os.environ["LANGSMITH_API_KEY"] = final_api_key
    os.environ["LANGSMITH_PROJECT"] = final_project
    os.environ["LANGSMITH_ENDPOINT"] = endpoint
    
    if tracing and final_api_key:
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        print(f"LangSmith tracing ENABLED")
        print(f"Project: {final_project}")
        print(f"View traces: https://smith.langchain.com/")
    else:
        os.environ["LANGSMITH_TRACING"] = "false"
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        if not final_api_key:
            print("LangSmith tracing DISABLED (no API key provided)")
        else:
            print("LangSmith tracing DISABLED")

# Auto-enable tracing on import (only if API key is provided)
if LANGSMITH_API_KEY:
    configure_langsmith()

# Load Google API key from environment variable
# Will be initialized when needed, not at import time
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
client = None

def get_client():
    """Get or create Google GenAI client. Raises error if API key is not set."""
    global client
    if client is None:
        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. "
                "Please set it in your .env file or environment variables."
            )
        client = genai.Client(api_key=GOOGLE_API_KEY)
    return client

# ============== WORKER POOL CONFIGURATION (FIFO) ==============

class WorkerPool:
    """
    Singleton class to manage concurrent workers with FIFO ordering.
    Includes rate limiting delay between API calls.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, max_workers: int = 3, delay_seconds: float = 5.0):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init(max_workers, delay_seconds)
        return cls._instance
    
    def _init(self, max_workers: int, delay_seconds: float = 5.0):
        self._max_workers = max_workers
        self._delay_seconds = delay_seconds  # Delay between requests
        self._semaphore = threading.Semaphore(max_workers)
        self._queue_lock = threading.Lock()
        self._queue_condition = threading.Condition(self._queue_lock)
        self._ticket_counter = 0
        self._current_serving = 0
        self._active_workers = 0
        self._last_request_time = 0  # Track last request time for rate limiting
    
    @classmethod
    def set_max_workers(cls, max_workers: int, delay_seconds: float = 5.0):
        with cls._lock:
            cls._instance = None
        return cls(max_workers, delay_seconds)
    
    @classmethod
    def set_delay(cls, delay_seconds: float):
        """Set delay between API requests"""
        if cls._instance:
            cls._instance._delay_seconds = delay_seconds
            print(f"Request delay set to {delay_seconds}s")
    
    @classmethod
    def reset(cls):
        with cls._lock:
            if cls._instance:
                cls._instance._ticket_counter = 0
                cls._instance._current_serving = 0
                cls._instance._active_workers = 0
                cls._instance._last_request_time = 0
    
    def acquire(self) -> int:
        with self._queue_lock:
            my_ticket = self._ticket_counter
            self._ticket_counter += 1
        
        with self._queue_condition:
            while my_ticket != self._current_serving:
                self._queue_condition.wait()
        
        self._semaphore.acquire()
        
        # Rate limiting: wait if last request was too recent
        with self._queue_lock:
            elapsed = time.time() - self._last_request_time
            if elapsed < self._delay_seconds and self._last_request_time > 0:
                wait_time = self._delay_seconds - elapsed
                print(f"Rate limit: waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
            self._last_request_time = time.time()
        
        with self._queue_condition:
            self._current_serving += 1
            self._active_workers += 1
            self._queue_condition.notify_all()
        
        return my_ticket
    
    def release(self):
        with self._queue_condition:
            self._active_workers -= 1
        self._semaphore.release()
    
    def __enter__(self):
        self._my_ticket = self.acquire()
        return self
    
    def __exit__(self, *args):
        self.release()

# Initialize default worker pool
# Initialize with 5 second delay between requests (rate limiting)
worker_pool = WorkerPool(max_workers=1, delay_seconds=20.0)

# ============== STATE DEFINITIONS ==============

class ContextItem(TypedDict):
    context: str
    review: str
    suggestions: list[str]
    is_approved: bool  # True if suggestions is empty
    iteration_count: int

class MCQItem(TypedDict):
    mcq: MCQ
    context: str
    context_index: int
    review: str
    suggestions: list[str]
    is_approved: bool

class GraphState(TypedDict):
    """Main graph state"""
    text: str
    number_contexts: int
    subject: str
    topic: str
    key_point: str
    exercises: str
    bloom_level: str
    model: str
    
    # Data - NOT using reducers for simpler control
    contexts: list[ContextItem]
    mcqs: list[MCQItem]
    
    # Control
    human_feedback: str
    current_stage: str
    context_iteration: int
    mcq_iteration: int
    max_iterations: int

# ============== NODE FUNCTIONS ==============

def generate_contexts(state: GraphState) -> dict:
    """Generate initial contexts from text"""
    print(f"[generate_contexts] Generating {state['number_contexts']} contexts...")
    
    contexts_list = gen_context(
        text=state['text'],
        subject=state['subject'],
        topic=state['topic'],
        number_context=state['number_contexts'],
        bloom_level=state['bloom_level'],
        client=get_client(),
        key_point=state.get('key_point', ''),
        exercises=state.get('exercises', ''),
        MODEL=state.get('model', 'gemini-2.5-flash')
    )
    
    context_items = [
        {
            "context": ctx,
            "review": "",
            "suggestions": [],
            "is_approved": False,
            "iteration_count": 0
        }
        for ctx in contexts_list
    ]
    
    print(f"[generate_contexts] Generated {len(context_items)} contexts")
    return {
        "contexts": context_items,
        "current_stage": "context_review"
    }

def review_all_contexts(state: GraphState) -> dict:
    """Review all contexts in parallel (with worker pool limit)"""
    print(f"[review_all_contexts] Reviewing {len(state['contexts'])} contexts...")
    
    contexts = state['contexts']
    updated_contexts = []
    
    def review_one(idx: int, ctx: ContextItem) -> ContextItem:
        # Skip already approved contexts
        if ctx['is_approved']:
            print(f"  Context {idx}: Already approved, skipping")
            return ctx
        
        with worker_pool:
            print(f"  Context {idx}: Reviewing...")
            review_result: Review = review_context(
                context_gen=ctx['context'],
                text=state['text'],
                client=get_client(),
                subject=state['subject'],
                topic=state['topic'],
                bloom_level=state['bloom_level'],
                key_point=state.get('key_point', ''),
                exercise=state.get('exercises', ''),
                MODEL=state.get('model', 'gemini-2.5-flash')
            )
        
        is_approved = len(review_result.suggestions) == 0
        print(f"  Context {idx}: {'Approved' if is_approved else f'Needs refine ({len(review_result.suggestions)} suggestions)'}")
        
        return {
            **ctx,
            "review": review_result.evaluation,
            "suggestions": review_result.suggestions,
            "is_approved": is_approved
        }
    
    # Process in parallel using threads
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(review_one, i, ctx): i for i, ctx in enumerate(contexts)}
        results = [None] * len(contexts)
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    
    return {"contexts": results}

def refine_contexts(state: GraphState) -> dict:
    """Refine contexts that have suggestions"""
    print(f"[refine_contexts] Refining contexts with suggestions...")
    
    contexts = state['contexts']
    updated_contexts = []
    
    def refine_one(idx: int, ctx: ContextItem) -> ContextItem:
        # Skip approved contexts
        if ctx['is_approved']:
            return ctx
        
        # Skip if max iterations reached
        if ctx['iteration_count'] >= state.get('max_iterations', 3):
            print(f"  Context {idx}: Max iterations reached, forcing approval")
            return {**ctx, "is_approved": True, "suggestions": []}
        
        with worker_pool:
            print(f"  Context {idx}: Refining (iteration {ctx['iteration_count'] + 1})...")
            refined: RefinedContext = refine_context(
                context=ctx['context'],
                context_review="\n".join(ctx['suggestions']),
                text=state['text'],
                client=get_client(),
                subject=state['subject'],
                topic=state['topic'],
                bloom_level=state['bloom_level'],
                key_point=state.get('key_point', ''),
                exercises=state.get('exercises', ''),
                MODEL=state.get('model', 'gemini-2.5-flash')
            )
        
        return {
            "context": refined.context_new,
            "review": "",
            "suggestions": [],
            "is_approved": False,  # Will be checked in next review
            "iteration_count": ctx['iteration_count'] + 1
        }
    
    # Process in parallel
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(refine_one, i, ctx): i for i, ctx in enumerate(contexts)}
        results = [None] * len(contexts)
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    
    return {
        "contexts": results,
        "context_iteration": state.get('context_iteration', 0) + 1
    }

def generate_mcqs(state: GraphState) -> dict:
    """Generate MCQs from approved contexts"""
    print(f"[generate_mcqs] Generating MCQs from {len(state['contexts'])} contexts...")
    
    contexts = state['contexts']
    mcqs = []
    
    def gen_one(idx: int, ctx: ContextItem) -> MCQItem:
        with worker_pool:
            print(f"  MCQ {idx}: Generating...")
            mcq_result: MCQ = gen_mcq(
                context=ctx['context'],
                bloom_level=state['bloom_level'],
                client=get_client(),
                MODEL=state.get('model', 'gemini-2.5-flash')
            )
        
        return {
            "mcq": mcq_result,
            "context": ctx['context'],
            "context_index": idx,
            "review": "",
            "suggestions": [],
            "is_approved": False
        }
    
    # Process in parallel
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(gen_one, i, ctx): i for i, ctx in enumerate(contexts)}
        results = [None] * len(contexts)
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    
    print(f"[generate_mcqs] Generated {len(results)} MCQs")
    return {
        "mcqs": results,
        "current_stage": "mcq_review"
    }

def review_all_mcqs(state: GraphState) -> dict:
    """Review all MCQs in parallel"""
    print(f"[review_all_mcqs] Reviewing {len(state['mcqs'])} MCQs...")
    
    mcqs = state['mcqs']
    
    def review_one(idx: int, mcq_item: MCQItem) -> MCQItem:
        if mcq_item['is_approved']:
            print(f"  MCQ {idx}: Already approved, skipping")
            return mcq_item
        
        with worker_pool:
            print(f"  MCQ {idx}: Reviewing...")
            review_result: Review = review_mcq(
                mcq=mcq_item['mcq'],
                client=get_client(),
                context=mcq_item['context'],
                bloom_level=state['bloom_level'],
                MODEL=state.get('model', 'gemini-2.5-flash')
            )
        
        is_approved = len(review_result.suggestions) == 0
        print(f"  MCQ {idx}: {'Approved' if is_approved else f'Needs refine ({len(review_result.suggestions)} suggestions)'}")
        
        return {
            **mcq_item,
            "review": review_result.evaluation,
            "suggestions": review_result.suggestions,
            "is_approved": is_approved
        }
    
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(review_one, i, mcq): i for i, mcq in enumerate(mcqs)}
        results = [None] * len(mcqs)
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    
    return {"mcqs": results}

def refine_mcqs_node(state: GraphState) -> dict:
    """Refine MCQs that have suggestions (node function)"""
    print(f"[refine_mcqs_node] Refining MCQs with suggestions...")
    
    mcqs = state['mcqs']
    mcq_iteration = state.get('mcq_iteration', 0)
    max_iter = state.get('max_iterations', 3)
    
    def refine_one(idx: int, mcq_item: MCQItem) -> MCQItem:
        if mcq_item['is_approved']:
            return mcq_item
        
        # Force approval if max iterations
        if mcq_iteration >= max_iter:
            print(f"  MCQ {idx}: Max iterations reached, forcing approval")
            return {**mcq_item, "is_approved": True, "suggestions": []}
        
        with worker_pool:
            print(f"  MCQ {idx}: Refining...")
            try:
                refined: RefinedMCQ = refine_mcqs_api(
                    mcq_gen=mcq_item['mcq'],
                    mcq_review="\n".join(mcq_item['suggestions']),
                    context=mcq_item['context'],
                    bloom_level=state['bloom_level'],
                    client=get_client(),
                    MODEL=state.get('model', 'gemini-2.5-flash')
                )
            except Exception as e:
                print(f"  MCQ {idx}: refine error -> {e}")
                # Mark approved to avoid blocking pipeline; keep original mcq
                return {
                    **mcq_item,
                    "review": f"Refine error: {e}",
                    "suggestions": [],
                    "is_approved": True
                }
        
        return {
            **mcq_item,
            "mcq": MCQ(question=refined.mcq_new),
            "review": "",
            "suggestions": [],
            "is_approved": False
        }
    
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(refine_one, i, mcq): i for i, mcq in enumerate(mcqs)}
        results = [None] * len(mcqs)
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    
    return {
        "mcqs": results,
        "mcq_iteration": mcq_iteration + 1
    }

def complete(state: GraphState) -> dict:
    """Mark workflow as complete"""
    print("[complete] Workflow complete!")
    return {"current_stage": "complete"}

# ============== ROUTING FUNCTIONS ==============

def should_refine_contexts(state: GraphState) -> Literal["refine", "generate_mcqs"]:
    """Check if any context needs refinement"""
    needs_refine = any(not ctx['is_approved'] for ctx in state['contexts'])
    max_iter = state.get('max_iterations', 3)
    current_iter = state.get('context_iteration', 0)
    
    if needs_refine and current_iter < max_iter:
        return "refine"
    return "generate_mcqs"

def should_refine_mcqs(state: GraphState) -> Literal["refine", "complete"]:
    """Check if any MCQ needs refinement"""
    needs_refine = any(not mcq['is_approved'] for mcq in state['mcqs'])
    max_iter = state.get('max_iterations', 3)
    current_iter = state.get('mcq_iteration', 0)
    
    if needs_refine and current_iter < max_iter:
        return "refine"
    return "complete"

# ============== BUILD THE GRAPH ==============

def build_mcq_graph():
    """
    Build MCQ generation graph with Batch Mode + Loop:
    
    Flow:
    1. Generate Contexts
    2. Review ALL Contexts
    3. Any needs refine? → Refine → Back to Review
    4. All approved → Generate MCQs
    5. Review ALL MCQs
    6. Any needs refine? → Refine → Back to Review
    7. All approved → Complete
    """
    
    builder = StateGraph(GraphState)
    
    # Add nodes
    builder.add_node("generate_contexts", generate_contexts)
    builder.add_node("review_contexts", review_all_contexts)
    builder.add_node("refine_contexts", refine_contexts)
    builder.add_node("generate_mcqs", generate_mcqs)
    builder.add_node("review_mcqs", review_all_mcqs)
    builder.add_node("refine_mcqs_node", refine_mcqs_node)
    builder.add_node("complete", complete)
    
    # Define edges
    builder.add_edge(START, "generate_contexts")
    builder.add_edge("generate_contexts", "review_contexts")
    
    # Context review → refine or generate MCQs
    builder.add_conditional_edges(
        "review_contexts",
        should_refine_contexts,
        {
            "refine": "refine_contexts",
            "generate_mcqs": "generate_mcqs"
        }
    )
    
    # After refine → back to review
    builder.add_edge("refine_contexts", "review_contexts")
    
    # Generate MCQs → review MCQs
    builder.add_edge("generate_mcqs", "review_mcqs")
    
    # MCQ review → refine or complete
    builder.add_conditional_edges(
        "review_mcqs",
        should_refine_mcqs,
        {
            "refine": "refine_mcqs_node",
            "complete": "complete"
        }
    )
    
    # After MCQ refine → back to review
    builder.add_edge("refine_mcqs_node", "review_mcqs")
    
    # Complete → END
    builder.add_edge("complete", END)
    
    # Compile
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    
    return graph

# ============== HELPER FUNCTIONS ==============

def set_max_workers(max_workers: int, delay_seconds: float = 5.0):
    """
    Set the maximum number of concurrent API calls and delay between requests.
    
    Args:
        max_workers: Maximum concurrent API calls
        delay_seconds: Delay between each request (default: 5.0s for rate limiting)
    """
    global worker_pool
    worker_pool = WorkerPool.set_max_workers(max_workers, delay_seconds)
    print(f"Worker pool updated: max_workers={max_workers}, delay={delay_seconds}s")

def run_mcq_generation(
    text: str,
    subject: str,
    topic: str,
    bloom_level: str,
    number_contexts: int = 3,
    key_point: str = "",
    exercises: str = "",
    model: str = "gemini-2.5-flash",
    max_iterations: int = 3,
    max_workers: int = 3,
    delay_seconds: float = 5.0
):
    """
    Run the MCQ generation workflow.
    
    Args:
        text: Source text for generating MCQs
        subject: Subject area
        topic: Specific topic
        bloom_level: Bloom's taxonomy level
        number_contexts: Number of contexts (= number of MCQs)
        key_point: Key points to focus on
        exercises: Related exercises
        model: Model to use
        max_iterations: Maximum refinement iterations
        max_workers: Maximum concurrent API calls
        delay_seconds: Delay between API requests (default: 5.0s for rate limiting)
    
    Returns:
        Final state with generated MCQs
    """
    # Reset and configure worker pool
    WorkerPool.reset()
    set_max_workers(max_workers, delay_seconds)
    
    graph = build_mcq_graph()
    
    initial_state = {
        "text": text,
        "subject": subject,
        "topic": topic,
        "bloom_level": bloom_level,
        "number_contexts": number_contexts,
        "key_point": key_point,
        "exercises": exercises,
        "model": model,
        "max_iterations": max_iterations,
        "contexts": [],
        "mcqs": [],
        "human_feedback": "",
        "current_stage": "start",
        "context_iteration": 0,
        "mcq_iteration": 0
    }
    thread_id = str(uuid.uuid4())
    
    config = {"configurable": {"thread_id": thread_id}}
    
    result = graph.invoke(initial_state, config)
    
    return result


# ============== MAIN ==============

if __name__ == "__main__":
    sample_text = """
    Machine Learning is a subset of artificial intelligence that enables 
    systems to learn and improve from experience without being explicitly programmed.
    The main types include supervised learning, unsupervised learning, and reinforcement learning.
    """
    
    graph = build_mcq_graph()
    
    # Visualize
    try:
        print("=== Graph Structure (Mermaid) ===")
        print(graph.get_graph().draw_mermaid())
    except Exception as e:
        print(f"Could not draw graph: {e}")
    # Run
    print("\n=== Running MCQ Generation ===")
    result = run_mcq_generation(
        text=sample_text,
        subject="Computer Science",
        topic="Machine Learning",
        key_point="Key points to focus on",
        bloom_level="Understanding",
        number_contexts=2,
        max_iterations=2,
        model="gemini-2.5-flash",
        max_workers=1,
        delay_seconds=10,
        config={'configurable': {'thread_id': 'mcq-gen-1'}}
    )
    
    print("\n=== Final Results ===")
    print(f"Generated {len(result.get('mcqs', []))} MCQs")
    for i, mcq in enumerate(result.get('mcqs', [])):
        print(f"\nMCQ {i+1}:")
        q = mcq['mcq'].question if hasattr(mcq['mcq'], 'question') else mcq['mcq']
        print(f"  Question: {q.stem[:100]}...")
        print(f"  Approved: {mcq['is_approved']}")

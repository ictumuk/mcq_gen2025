import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]  # .../ai2025
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent)) 
from prompt.refine_prompt import refine_mcqs_prompt, refine_context_prompt
from .gen import Question
from pydantic import BaseModel

class RefinedMCQ(BaseModel):
    mcq_new:Question

class RefinedContext(BaseModel):
    context_new:str
    refinement:str

def refine_context(context, context_review, text, client,subject, topic, bloom_level,
                       key_point:str = "",
                       exercises:str = "",
                       MODEL = "gemini-2.5-flash"):
    """
    refine_context refines the generated context based on the original context and specified parameters.
    Args:
        context (str): The context generated previously.
        context_review (str): The original context to be refined.
        text (str): Lecture content originally provided.
        subject (str): The subject area of the context.
        topic (str): The specific topic within the subject.
        key_point (str): Key points to focus on during refinement.
        exercises (str): Exercises to consider during refinement.
        bloom_level (str): Bloom's taxonomy level to target.
        client: The Google GenAI client instance.
        MODEL (str): The model to use for generation.
    Returns:
        Context: A refined context object.
    """
    refine_context_template = refine_context_prompt.format(
        context=context,
        context_review=context_review,
        text=text,
        subject=subject,
        topic=topic,
        key_point=key_point,
        exercises=exercises,
        bloom_level=bloom_level,
    )
    response = client.models.generate_content(
        model=MODEL,
        config={
            "response_mime_type": "application/json",
            "response_schema": RefinedContext,
        },
        contents=refine_context_template,
    )
    if isinstance(response, tuple):
        response = response[0]
    refine_result: RefinedContext = response.parsed
    return refine_result

def refine_mcqs(mcq_gen, mcq_review, context, bloom_level, client,
                 MODEL = "gemini-2.5-flash"):
    """
    refine_mcqs refines the generated MCQs based on the original MCQs and specified parameters.
    Args:
        mcq(str): The MCQs generated previously.
        review (str): The original MCQs to be refined.
        context (str): The context related to the MCQs.
        bloom_level (str): Bloom's taxonomy level to target.
        client: The Google GenAI client instance.
        MODEL (str): The model to use for generation.
    Returns:
        Question: A refined MCQ object.
    """
    refine_mcqs_template = refine_mcqs_prompt.format(
        mcq=mcq_gen,
        review=mcq_review,
        context=context,
        bloom_level=bloom_level,
    )
    response = client.models.generate_content(
        model=MODEL,
        config={
            "response_mime_type": "application/json",
            "response_schema": RefinedMCQ,
        },
        contents=refine_mcqs_template,
    )
    if isinstance(response, tuple):
        response = response[0]
    refine_result: RefinedMCQ = response.parsed
    return refine_result

# if __name__ == "__main__":
#     import sys
#     from pathlib import Path
#     from google import genai

#     # Thêm path để import được prompt/*
#     ROOT = Path(__file__).resolve().parents[1]  # ai2025/
#     sys.path.insert(0, str(ROOT))
#     sys.path.insert(0, str(ROOT.parent))  # MCQs/

#     # Tạo client (điền API key)
#     GOOGLE_API_KEY = "AIzaSyD1UrY-y8L1ljWXwNd2AVxv8F5UYmpHiV8"
#     client = genai.Client(api_key=GOOGLE_API_KEY)

#     # Ví dụ tối giản: dùng cùng MCQ giả lập như đã test trong notebook
#     from graph.gen import MCQ, Question, Options, option, Reason

#     sample_mcq = MCQ(
#         question=Question(
#             stem="So sánh hành vi do-while lồng nhau với điều kiện a<=2, b<=3",
#             options=Options(options=[
#                 option(id="A", text="In (1,1)(1,2)(1,3)(2,1)(2,2)(2,3)"),
#                 option(id="B", text="In (1,1)(2,1)(1,2)(2,2)(1,3)(2,3)"),
#                 option(id="C", text="In vô hạn"),
#                 option(id="D", text="Không in gì"),
#             ]),
#             correct_answer="A",
#             reasoning=Reason(
#                 bloom_level_analysis="Apply",
#                 tactic_analysis="Hardness-first nested loop trace",
#                 answer_justification="Theo trace do-while, b chạy 1..3 mỗi a, rồi a++ đến 3 thì dừng",
#                 distractor_justification=[
#                     option(id="A", text="Đáp án đúng"),
#                     option(id="B", text="Nhầm thứ tự do-while"),
#                     option(id="C", text="Nhầm điều kiện dừng"),
#                     option(id="D", text="Nhầm không vào vòng"),
#                 ],
#             ),
#         )
#     )

#     from prompt.refine_prompt import refine_mcqs_prompt
#     # Gọi refine_mcqs
#     from graph.refine import refine_mcqs

#     result = refine_mcqs(
#             mcq_gen=sample_mcq,
#             mcq_review="Refine to avoid vague reference; modify loop bounds to require actual tracing.",
#             context="Vòng lặp do...while lồng nhau; ví dụ a<=2, b<=3.",
#             bloom_level="Apply",
#             client=client,
#             MODEL="gemini-2.5-flash",
#         )
#     print("Parsed:", result)
    

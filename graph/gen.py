from prompt.context_prompt import ctx_prompt
from prompt.stem_prompt import stem_gen_prompt
from pydantic import BaseModel
from google import genai


class Context(BaseModel):
    context: str

class Contexts(BaseModel):
    contexts: list[Context]

class option(BaseModel):
    id: str
    text: str

class Options(BaseModel):
    options: list[option]

class Reason(BaseModel):
    bloom_level_analysis:str
    tactic_analysis: str
    answer_justification: str
    distractor_justification: list[option]

class Question(BaseModel):
    stem: str
    options: Options
    correct_answer: str
    reasoning: Reason

class MCQ(BaseModel):
    question: Question

def gen_mcq(context, bloom_level, client, num_questions: int = 1,
             MODEL = "gemini-2.5-flash") -> MCQ:
    """
    gen_mcq generates a multiple-choice question (MCQ) based on the provided context and parameters.
    Args:
        context (str): The context to generate the question from.
        subject (str): The subject area of the question.
        topic (str): The specific topic within the subject.
        bloom_level (str): Bloom's taxonomy level to target. (e.g., "Remembering", "Understanding", etc.)
        client: The Google GenAI client instance.
        MODEL (str): The model to use for generation.
    Returns:
        MCQ: A multiple-choice question object.
        MCQ schema:
        {
            "question": {
                "stem": str,
                "options": {
                    "options": [
                        {"id": str,
                        "text": str},
                        ...
                    ]
                },
                "correct_answer": str,
                "reasoning": {
                    "bloom_level_analysis": str,
                    "tactic_analysis": str,
                    "answer_justification": str,
                    "distractor_justification": [
                        {"id": str,
                        "text": str},
                        ...
                    ]
                }
            }
        }
    """
    mcq_template = stem_gen_prompt.format(
        context=context,
        num_questions=num_questions,
        bloom_level=bloom_level
    )
    result = client.models.generate_content(
        model=MODEL,
        contents=mcq_template,
        config={
            "response_mime_type": "application/json",
            "response_schema": MCQ,
        },
    )
    if isinstance(result, tuple):
        result = result[0]
    my_mcq: MCQ = result.parsed
    return my_mcq

def gen_context(text, subject, topic, number_context, bloom_level, client,
                key_point: str = "",
                exercises: str = "",
                MODEL = "gemini-2.5-flash") -> list[str]:
    """
    gen_context generates a list of contexts based on the provided parameters.
    Args:
        text (str): The main text to generate contexts from.
        subject (str): The subject area of the text.
        topic (str): The specific topic within the subject.
        key_point (str): Key points to focus on.
        exercises (str): Exercises related to the text.
        number_context (int): Number of contexts to generate.
        bloom_level (str): Bloom's taxonomy level to target. (e.g., "Remembering", "Understanding", etc.)
        client: The Google GenAI client instance.
        MODEL (str): The model to use for generation.
    Returns:
        List[str]: A list of generated contexts.
    """
    ctx_template = ctx_prompt.format(
        text=text,
        subject=subject,
        topic=topic,
        key_point=key_point,
        exercises=exercises,
        number_context=number_context,
        bloom_level=bloom_level
    )
    result = client.models.generate_content(
        model=MODEL,
        contents=ctx_template,
        config={
            "response_mime_type": "application/json",
            "response_schema": Contexts,
        },
    )
    if isinstance(result, tuple):
        result = result[0]

    my_contexts: Contexts = result.parsed.contexts
    contexts = [x.context for x in my_contexts]

    return contexts

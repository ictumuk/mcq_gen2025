from pydantic import BaseModel
from google import genai
from prompt.review_prompt import review_context_prompt, review_mcq_prompt

class Review(BaseModel):
    evaluation: str
    suggestions: list[str]

def review_context(context_gen, text, client, subject, topic,
                   bloom_level,
                   exercise: str = "",
                   key_point: str = "",
                   MODEL = "gemini-2.5-flash") -> Review:
    review_context_template = review_context_prompt.format(context_gen=context_gen,
                                                              text=text,
                                                              subject=subject,
                                                              topic=topic,
                                                              bloom_level=bloom_level,
                                                              exercise=exercise,
                                                              key_point=key_point)
    result = client.models.generate_content(
        model=MODEL,
        config={
            "response_mime_type": "application/json",
            "response_schema": Review,
        },
        contents=review_context_template,
    )
    if isinstance(result, tuple):
        result = result[0]
    my_review: Review = result.parsed
    return my_review

def review_mcq(mcq, client, context, bloom_level,
                MODEL = "gemini-2.5-flash") -> Review:
    review_mcq_template = review_mcq_prompt.format(mcq = mcq,
                                                    context = context,
                                                    bloom_level = bloom_level)
    result = client.models.generate_content(
        model=MODEL,
        config={
            "response_mime_type": "application/json",
            "response_schema": Review,
        },
        contents=review_mcq_template,
    )
    if isinstance(result, tuple):
        result = result[0]

    my_review: Review = result.parsed
    return my_review

if __name__ == "__main__":
    # print(review_context_prompt)
    print(review_mcq_prompt)

import os
import instructor
from openai import OpenAI
from models import TailoredCV

def tailor_cv(parsed_cv: TailoredCV, job_description: str) -> TailoredCV:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is missing from environment variables.")

    client = instructor.from_openai(
        OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        ),
        mode=instructor.Mode.JSON
    )

    print("Tailoring profile and experience to match the Job Description...")

    system_prompt = (
        "You are an expert technical recruiter and resume writer. Your absolute priority is to adapt the candidate's "
        "Professional Summary and Technical Skills to directly highlight how their background fits the target Job Description.\n\n"
        "Guidelines:\n"
        "1. Rewrite the Professional Summary to directly address the core needs of the Job Description (e.g., if they ask for automation, APIs, or specific frameworks, explain how the candidate's Python and AI foundation applies to that).\n"
        "2. Dynamically update the 'Technical Skills' section. Keep the candidate's core technologies but prioritize and rephrase them to use the language, keywords, and tools requested in the JD (e.g., REST APIs, integrations, automation workflows) where logically applicable to a Data Science/AI background.\n"
        "3. Maintain 100% factual accuracy. Do NOT invent new job titles, change employment dates, or fake university degrees. Optimize the phrasing and framing, not the facts."
    )

    tailored_output = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        response_model=TailoredCV,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Target Job Description:\n{job_description}\n\nCandidate JSON Structure:\n{parsed_cv}"
            }
        ]
    )

    return tailored_output
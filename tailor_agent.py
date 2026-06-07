import os
import instructor
from openai import OpenAI
from models import TailoredCV

def tailor_cv(raw_cv_text: str, job_description: str) -> TailoredCV:
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

    print("Tailoring profile and experience dynamically based on full CV text...")

    system_prompt = """
You are a World-Class Executive Tech Resume Designer and AI Recruiter. 
Your task is to review the candidate's complete, raw CV text and completely restructure, upgrade, and tailor it to match the target Job Description (JD) with maximum creative freedom.

Strict Content & Formatting Guidelines:
1. **Dynamic Reprioritization (Crucial):** Look at the entire CV. If a high-value technical training (like HTU), bootcamp, or major AI project is listed under Education or another section, MOVE IT to the very top of the Experience section to show tech relevance immediately.
2. **De-emphasize Non-Technical Roles:** Drastically shrink non-technical or volunteer roles (like TEDx, student club leadership, or community volunteering). Combine or compress them into a bare minimum (1 short bullet point each max) under a secondary section, just to show leadership. Save 80% of the CV space for technical impact.
3. **Creative & High-Impact Rephrasing:** Do not stick to the original dry wording. Completely rewrite the Professional Summary and Experience bullet points using powerful technical action verbs, highlighting core frameworks (e.g., LLMs, RAG, Computer Vision) and engineering impact.
4. **Factual Anchor Guardrail:** You have total freedom in wording, structural placement, and impact framing. However, you MUST NOT invent new employers, job titles, employment dates, or university degrees. Everything must be anchored in the candidate's real history.
"""

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
                "content": f"Target Job Description:\n{job_description}\n\nCandidate's Full Raw CV Text:\n{raw_cv_text}"
            }
        ]
    )

    return tailored_output
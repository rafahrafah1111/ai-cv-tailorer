import os
import instructor
from openai import OpenAI
from models import TailoredCV
from extractor import extract_text_from_pdf

def parse_pdf_to_json(pdf_path: str) -> TailoredCV:
    raw_text = extract_text_from_pdf(pdf_path)
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is missing from environment variables.")

    client = instructor.from_openai(
        OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        ),
        mode=instructor.Mode.JSON
    )
    
    print("Analyzing CV using OpenRouter (deepseek-chat)...")
    
    structured_cv = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        response_model=TailoredCV,
        messages=[
            {
                "role": "system",
                "content": "You are an expert data parser. Map the raw CV text perfectly into the structured schema provided. Do not invent any information."
            },
            {
                "role": "user",
                "content": f"Here is the raw CV text:\n\n{raw_text}"
            }
        ],
        temperature=0.0
    )
    
    return structured_cv

if __name__ == "__main__":
    my_pdf = "CV Rafah Al Nabulsy (10).pdf"
    
    try:
        cv_json = parse_pdf_to_json(my_pdf)
        print("CV successfully parsed to Structured JSON:")
        print(cv_json.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error running OpenRouter API: {e}")
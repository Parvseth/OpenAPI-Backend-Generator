from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_route_logic(prompt: str, model: str = "llama3-70b-8192") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert backend engineer. Write clean, FastAPI + SQLAlchemy Python code."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=400
    )
    return response.choices[0].message.content.strip()

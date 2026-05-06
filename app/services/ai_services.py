import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_checkin(answers):

    prompt = f"""
    Você é um especialista em bem-estar corporativo.

    Analise as respostas abaixo:

    {answers}

    Responda APENAS em JSON válido:

    {{
      "overall_mood": "positivo | neutro | negativo | crítico",
      "ai_insights": "texto curto em português"
    }}
    """

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    response_text = response.text.replace("```json", "").replace("```", "").strip()

    return json.loads(response_text)

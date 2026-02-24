import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

def gerar_resposta(prompt, temperature=0.2):
    resposta = client.models.generate_content(
        # GARANTA QUE O MODELO ESTÁ EXATAMENTE ASSIM:
        model="gemini-2.5-flash", 
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
        )
    )
    return resposta.text
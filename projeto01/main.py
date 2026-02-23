import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carrega as variáveis de ambiente
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Inicializa o cliente Gemini com a chave de API
client = genai.Client(api_key=gemini_api_key)

# Teste simples
resposta = client.models.generate_content(
    model="gemini-2.5-flash", # Equivalente ao gpt-4o-mini (rápido, barato e eficiente)
    contents="Explique IA Generativa para um diretor técnico, focando em riscos e arquitetura. Resultado em 3 parágrafos.",
    config=types.GenerateContentConfig(
        system_instruction="Você é um assistente técnico.",
        temperature=0.7,
    )
)

# Imprime o resultado
print(resposta.text)
# classifier.py
from llm_client import gerar_resposta
import validator
import injection_guard
import embeddings

def classificar_mensagem(mensagem: str, temperature: float = 0.2, usar_rag: bool = True) -> dict:

    # ── 1. PROTEÇÃO: detecta prompt injection antes de tudo ──
    if injection_guard.detectar_injection(mensagem):
        return injection_guard.erro_injection()

    # ── 2. RAG: busca contexto relevante na base vetorial ──
    contexto_rag = ""
    if usar_rag:
        try:
            contexto_rag = embeddings.buscar_contexto(mensagem, top_k=3)
        except RuntimeError:
            pass

    # ── 3. PROMPT: monta com ou sem contexto ──
    if contexto_rag:
        prompt = f"""
Você é um classificador de mensagens de atendimento ao cliente.
Use o contexto abaixo (extraído da base de conhecimento) para ajudar na classificação:
=== CONTEXTO ===
{contexto_rag}
================
Classifique a mensagem do cliente em uma das categorias: {', '.join(validator.CATEGORIAS_PERMITIDAS)}.
Retorne APENAS um JSON no formato:
{{
    "categoria": "nome_categoria"
}}
Mensagem do cliente: "{mensagem}"
"""
    else:
        prompt = f"""
Classifique a mensagem abaixo em uma das seguintes categorias: {', '.join(validator.CATEGORIAS_PERMITIDAS)}.
Retorne apenas um JSON no formato:
{{
    "categoria": "nome_categoria"
}}
Mensagem: "{mensagem}"
"""

    # ── 4. CHAMADA À API ──
    resposta_bruta = gerar_resposta(prompt, temperature)

    # temperatura alta pode retornar resposta vazia
    if not resposta_bruta or not resposta_bruta.strip():
        return validator.fallback_seguro(ValueError("Resposta vazia retornada pelo modelo"))

    try:
        # ── 5. PARSE E VALIDAÇÃO ──
        dados_json = validator.parse_json(resposta_bruta)
        dados_validados = validator.validar_categoria(dados_json)
        dados_validados["status"] = "sucesso"
        dados_validados["rag_usado"] = bool(contexto_rag)
        return dados_validados

    except Exception as erro:
        return validator.fallback_seguro(erro)
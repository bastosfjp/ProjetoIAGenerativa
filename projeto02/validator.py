import json

CATEGORIAS_PERMITIDAS = ["Suporte", "Vendas", "Financeiro", "Geral"]

def parse_json(texto_resposta):
    """Limpa a string e tenta converter para JSON"""
    texto = texto_resposta.strip()
    if texto.startswith("```json"):
        texto = texto[7:]
    if texto.endswith("```"):
        texto = texto[:-3]
    texto = texto.strip()

    try:
        return json.loads(texto)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido retornado pelo modelo: {e}")

def validar_categoria(dados_json):
    """Garante que a categoria não foi inventada"""
    if "categoria" not in dados_json:
        raise ValueError("Chave 'categoria' ausente no JSON.")
    
    categoria = dados_json["categoria"]
    if categoria not in CATEGORIAS_PERMITIDAS:
        raise ValueError(f"Categoria inventada pelo modelo: '{categoria}'")
    
    return dados_json

def fallback_seguro(erro):
    """Retorna um padrão seguro se algo der errado"""
    return {
        "categoria": "Geral", # Categoria padrão para erros
        "status": "falha_fallback",
        "detalhe_erro": str(erro)
    }
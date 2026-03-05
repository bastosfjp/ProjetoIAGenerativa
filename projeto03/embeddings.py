# embeddings.py
import os
import math
from sentence_transformers import SentenceTransformer
_modelo = SentenceTransformer("all-MiniLM-L6-v2")
# ─────────────────────────────────────────
# 1. CARREGA E DIVIDE O CONHECIMENTO.TXT
# ─────────────────────────────────────────

def carregar_chunks(caminho="conhecimento.txt", separador="\n\n"):
    """
    Lê o arquivo e divide em chunks por parágrafo/bloco.
    Filtra linhas vazias e separadores visuais (===, ---).
    """
    with open(caminho, "r", encoding="utf-8") as f:
        texto = f.read()

    chunks = []
    for bloco in texto.split(separador):
        bloco = bloco.strip()
        # ignora separadores visuais e blocos muito curtos
        if len(bloco) < 20 or set(bloco).issubset(set("=- \n")):
            continue
        chunks.append(bloco)
    return chunks


# ─────────────────────────────────────────
# 2. GERA EMBEDDING VIA GEMINI
# ─────────────────────────────────────────

def gerar_embedding(texto: str) -> list[float]:
    return _modelo.encode(texto).tolist()


# ─────────────────────────────────────────
# 3. ARMAZENA VETORES EM MEMÓRIA
# ─────────────────────────────────────────

# Estrutura: lista de dicts {"chunk": str, "vetor": list[float]}
_base_vetorial: list[dict] = []


def construir_base_vetorial(caminho="conhecimento.txt"):
    """
    Carrega os chunks, gera embeddings e armazena tudo em memória.
    Deve ser chamado UMA VEZ na inicialização do sistema.
    """
    global _base_vetorial
    print("📚 Construindo base vetorial...")
    chunks = carregar_chunks(caminho)

    _base_vetorial = []
    for i, chunk in enumerate(chunks):
        vetor = gerar_embedding(chunk)
        _base_vetorial.append({"chunk": chunk, "vetor": vetor})
        print(f"  ✅ Chunk {i+1}/{len(chunks)} indexado.")

    print(f"✔ Base pronta com {len(_base_vetorial)} chunks.\n")
    return _base_vetorial


# ─────────────────────────────────────────
# 4. BUSCA POR SIMILARIDADE (COSINE)
# ─────────────────────────────────────────

def _similaridade_cosseno(v1: list[float], v2: list[float]) -> float:
    """Calcula a similaridade de cosseno entre dois vetores."""
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def buscar_contexto(pergunta: str, top_k: int = 3) -> str:
    """
    Gera o embedding da pergunta e retorna os top_k chunks
    mais similares, concatenados como contexto.
    """
    if not _base_vetorial:
        raise RuntimeError("Base vetorial vazia. Chame construir_base_vetorial() primeiro.")

    vetor_pergunta = gerar_embedding(pergunta)

    # calcula similaridade com todos os chunks
    scores = [
        {
            "chunk": item["chunk"],
            "score": _similaridade_cosseno(vetor_pergunta, item["vetor"])
        }
        for item in _base_vetorial
    ]

    # ordena do mais similar para o menos
    scores.sort(key=lambda x: x["score"], reverse=True)
    top = scores[:top_k]

    contexto = "\n\n---\n\n".join(item["chunk"] for item in top)
    return contexto
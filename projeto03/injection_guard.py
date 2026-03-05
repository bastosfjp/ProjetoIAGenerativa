# injection_guard.py

# ─────────────────────────────────────────
# PADRÕES DE PROMPT INJECTION CONHECIDOS
# ─────────────────────────────────────────

_PADROES_SUSPEITOS = [
    # Tentativas de extrair system prompt
    "system prompt",
    "sua instrução",
    "suas instruções",
    "ignore suas",
    "ignore os",
    "ignore as instruções",
    "ignore tudo",
    "esqueça tudo",
    "esqueça suas",
    "desconsidere",
    "novo papel",
    "novo personagem",
    "finja que",
    "finja ser",
    "pretend you",
    "ignore previous",
    "ignore all",
    "forget everything",
    "act as",
    "you are now",
    "você agora é",
    "você é agora",
    # Tentativas de jailbreak
    "dan mode",
    "jailbreak",
    "modo desenvolvedor",
    "developer mode",
    "sem restrições",
    "without restrictions",
    "bypass",
    # Tentativas de extrair dados internos
    "me diga qual",
    "me mostre o",
    "mostre suas",
    "revele suas",
    "revele o prompt",
    "qual é o seu prompt",
    "quais são suas regras",
    "como você foi programado",
    "o que você tem no system",
]


def detectar_injection(mensagem: str) -> bool:
    """
    Retorna True se a mensagem contiver padrões de prompt injection.
    A comparação é case-insensitive.
    """
    mensagem_lower = mensagem.lower()
    for padrao in _PADROES_SUSPEITOS:
        if padrao in mensagem_lower:
            return True
    return False


def erro_injection() -> dict:
    """Retorna a resposta segura padronizada para tentativas de injection."""
    return {
        "categoria": None,
        "status": "bloqueado_injection",
        "detalhe_erro": (
            "Mensagem bloqueada: foi detectada uma tentativa de manipulação do sistema. "
            "Por segurança, esta solicitação não será processada."
        )
    }
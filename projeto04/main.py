from groq import Groq
from dotenv import load_dotenv
from memoria import GerenciadorMemoria
from tools import (
    data_atual,
    calcular_idade,
    converter_temperatura,
    calcular_imc,
    gerar_senha,
)
import os
import re

load_dotenv()

# ─────────────────────────────────────────
# Configuração do cliente Groq
# ─────────────────────────────────────────
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODELO = "llama-3.3-70b-versatile"

# ─────────────────────────────────────────
# Persona do assistente (System Prompt)
# ─────────────────────────────────────────
SYSTEM_PROMPT = """Você é o Logos, um assistente inteligente, direto e levemente bem-humorado.
Você fala português do Brasil de forma clara e objetiva.
Quando o usuário perguntar sobre data, idade, temperatura, IMC ou senha, 
você SEMPRE usa os resultados das funções Python fornecidos no contexto — nunca inventa esses valores.
Se uma função retornar um resultado, apresente-o de forma natural na resposta.
Mantenha respostas concisas, a menos que o usuário peça mais detalhes.
Você lembra do contexto da conversa e usa isso para dar respostas mais personalizadas."""

# ─────────────────────────────────────────
# Inicialização da memória
# ─────────────────────────────────────────
memoria = GerenciadorMemoria()

# Adiciona system prompt se ainda não estiver no histórico
if not any(m["role"] == "system" for m in memoria.obter_mensagens()):
    memoria.historico.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
    memoria.salvar_historico()


# ─────────────────────────────────────────
# Detector de intenção para funções Python
# ─────────────────────────────────────────
def detectar_e_executar_funcao(pergunta: str) -> str | None:
    """
    Detecta se a pergunta requer uma função Python e a executa.
    Retorna o resultado da função ou None se não for necessário.
    """
    p = pergunta.lower()

    # Data atual
    if any(w in p for w in ["que dia", "data de hoje", "data atual", "hoje é", "que horas"]):
        return f"[função: data_atual] {data_atual()}"

    # Calcular idade
    match_idade = re.search(r"(?:nasci|nasceu|nascida?|aniversário).{0,30}(\d{4})", p)
    if match_idade or ("idade" in p and re.search(r"\b(19|20)\d{2}\b", p)):
        anos = re.findall(r"\b(19|20)\d{2}\b", p)
        if anos:
            ano = int(anos[0])
            # Tenta extrair mês e dia se mencionados
            meses = re.findall(r"\b(0?[1-9]|1[0-2])\b", p)
            dias = re.findall(r"\b([0-2]?[0-9]|3[01])\b", p)
            mes = int(meses[0]) if meses else 1
            dia = int(dias[0]) if dias else 1
            return f"[função: calcular_idade] {calcular_idade(ano, mes, dia)}"

    # Converter temperatura
    match_temp = re.search(
        r"(\d+(?:[.,]\d+)?)\s*°?\s*([cfkCFK])\s*(?:para|em|->|→)\s*([cfkCFK])", p
    )
    if match_temp or ("converter" in p and any(u in p for u in ["celsius", "fahrenheit", "kelvin"])):
        if match_temp:
            valor = float(match_temp.group(1).replace(",", "."))
            de = match_temp.group(2)
            para = match_temp.group(3)
            return f"[função: converter_temperatura] {converter_temperatura(valor, de, para)}"

    # Calcular IMC
    match_imc = re.search(r"(\d+(?:[.,]\d+)?)\s*kg.{0,20}(\d+(?:[.,]\d+)?)\s*m", p)
    if "imc" in p or "índice de massa" in p:
        if match_imc:
            peso = float(match_imc.group(1).replace(",", "."))
            altura = float(match_imc.group(2).replace(",", "."))
            return f"[função: calcular_imc] {calcular_imc(peso, altura)}"
        else:
            # Tenta extrair números soltos
            nums = re.findall(r"\d+(?:[.,]\d+)?", p)
            if len(nums) >= 2:
                peso = float(nums[0].replace(",", "."))
                altura = float(nums[1].replace(",", "."))
                return f"[função: calcular_imc] {calcular_imc(peso, altura)}"

    # Gerar senha
    if any(w in p for w in ["gerar senha", "cria uma senha", "senha segura", "nova senha", "senha aleatória"]):
        tamanho_match = re.search(r"(\d+)\s*(?:caracteres|dígitos|letras)", p)
        tamanho = int(tamanho_match.group(1)) if tamanho_match else 12
        sem_especiais = "sem especiais" in p or "só letras" in p or "apenas letras" in p
        return f"[função: gerar_senha] {gerar_senha(tamanho, not sem_especiais)}"

    return None


# ─────────────────────────────────────────
# Função principal de chat
# ─────────────────────────────────────────
def chat(pergunta: str) -> str:
    resultado_funcao = detectar_e_executar_funcao(pergunta)

    if resultado_funcao:
        # Monta contexto enriquecido com o resultado da função
        conteudo_usuario = (
            f"{pergunta}\n\n"
            f"[Resultado automático da função Python]: {resultado_funcao.split('] ', 1)[-1]}"
        )
    else:
        conteudo_usuario = pergunta

    memoria.adicionar("user", conteudo_usuario)

    resposta = client.chat.completions.create(
        model=MODELO,
        messages=memoria.obter_mensagens(),
        temperature=0.7,
        max_tokens=1024,
    )

    resposta_conteudo = resposta.choices[0].message.content
    memoria.adicionar("assistant", resposta_conteudo)
    return resposta_conteudo


# ─────────────────────────────────────────
# Loop principal
# ─────────────────────────────────────────
def exibir_ajuda():
    print("""
┌─────────────────────────────────────────┐
│           LOGOS - Comandos              │
├─────────────────────────────────────────┤
│  /limpar   → Apaga o histórico          │
│  /ajuda    → Exibe esta mensagem        │
│  sair/exit → Encerra o programa         │
└─────────────────────────────────────────┘
""")


print("\n🤖 Logos iniciado! Digite /ajuda para ver os comandos.\n")
exibir_ajuda()

while True:
    try:
        pergunta = input("Você: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando o Nexus. Até mais!")
        break

    if not pergunta:
        continue

    # Comandos especiais
    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Logos: Até mais! 👋")
        break

    if pergunta.lower() == "/limpar":
        memoria.limpar()
        print("Logos: Memória da conversa apagada. ✨\n")
        continue

    if pergunta.lower() == "/ajuda":
        exibir_ajuda()
        continue

    # Processa a pergunta
    resposta = chat(pergunta)
    print(f"\nLogos: {resposta}\n")
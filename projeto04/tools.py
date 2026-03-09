import datetime
import random
import string
import math


def data_atual():
    """Retorna a data atual formatada."""
    hoje = datetime.date.today()
    dias = ["segunda-feira", "terça-feira", "quarta-feira",
            "quinta-feira", "sexta-feira", "sábado", "domingo"]
    dia_semana = dias[hoje.weekday()]
    return hoje.strftime(f"{dia_semana}, %d/%m/%Y")


def calcular_idade(ano_nascimento: int, mes_nascimento: int = 1, dia_nascimento: int = 1) -> str:
    """Calcula a idade de uma pessoa com base na data de nascimento."""
    hoje = datetime.date.today()
    nascimento = datetime.date(ano_nascimento, mes_nascimento, dia_nascimento)
    idade = hoje.year - nascimento.year - (
        (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
    )
    return f"{idade} anos"


def converter_temperatura(valor: float, de: str, para: str) -> str:
    """
    Converte temperatura entre Celsius, Fahrenheit e Kelvin.
    de/para: 'C', 'F' ou 'K'
    """
    de = de.upper().strip()
    para = para.upper().strip()

    # Converter tudo para Celsius primeiro
    if de == "C":
        celsius = valor
    elif de == "F":
        celsius = (valor - 32) * 5 / 9
    elif de == "K":
        celsius = valor - 273.15
    else:
        return "Escala inválida. Use C, F ou K."

    # Converter de Celsius para o destino
    if para == "C":
        resultado = celsius
    elif para == "F":
        resultado = (celsius * 9 / 5) + 32
    elif para == "K":
        resultado = celsius + 273.15
    else:
        return "Escala inválida. Use C, F ou K."

    nomes = {"C": "Celsius", "F": "Fahrenheit", "K": "Kelvin"}
    return f"{valor}°{de} = {resultado:.2f}°{para} ({nomes[de]} → {nomes[para]})"


def calcular_imc(peso_kg: float, altura_m: float) -> str:
    """Calcula o IMC e retorna o resultado com classificação."""
    if altura_m <= 0 or peso_kg <= 0:
        return "Valores inválidos para peso ou altura."
    imc = peso_kg / (altura_m ** 2)

    if imc < 18.5:
        classificacao = "Abaixo do peso"
    elif imc < 25:
        classificacao = "Peso normal"
    elif imc < 30:
        classificacao = "Sobrepeso"
    elif imc < 35:
        classificacao = "Obesidade grau I"
    elif imc < 40:
        classificacao = "Obesidade grau II"
    else:
        classificacao = "Obesidade grau III"

    return f"IMC: {imc:.2f} → {classificacao}"


def gerar_senha(tamanho: int = 12, usar_especiais: bool = True) -> str:
    """Gera uma senha aleatória segura."""
    caracteres = string.ascii_letters + string.digits
    if usar_especiais:
        caracteres += "!@#$%^&*()_+-=[]{}|"
    senha = ''.join(random.choices(caracteres, k=tamanho))
    return f"Senha gerada: {senha}"
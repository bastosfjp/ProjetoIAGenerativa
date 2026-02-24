from llm_client import gerar_resposta
import validator

def classificar_mensagem(mensagem, temperature=0.2):
    prompt = f"""
        Classifique a mensagem abaixo em uma das seguintes categorias: {', '.join(validator.CATEGORIAS_PERMITIDAS)}.
        Retorne apenas um JSON no formato:
        {{
            "categoria": "nome_categoria"
        }}

        Mensagem: "{mensagem}"
    """
    
    # 1. Chama a API
    resposta_bruta = gerar_resposta(prompt, temperature)
    
    try:
        # 2. Faz o parse e valida
        dados_json = validator.parse_json(resposta_bruta)
        dados_validados = validator.validar_categoria(dados_json)
        
        # 3. Se passou por tudo, sucesso!
        dados_validados["status"] = "sucesso"
        return dados_validados
        
    except Exception as erro:
        # 4. Se deu erro no parse ou na validação, chama o fallback
        return validator.fallback_seguro(erro)
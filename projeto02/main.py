from classifier import classificar_mensagem
import time
import sys

def rodar_mensagens_originais():
    print("\n=== TESTE DAS MENSAGENS ORIGINAIS ===")
    mensagens_cliente = [
        "Quero contratar o plano premium",
        "O sistema está com erro",
        "Quero cancelar minha assinatura",
        "Quero falar com um atendente",
        "Preciso de ajuda com meu pagamento",
        "Gostaria de atualizar minhas informações de conta",
        "Vocês trabalham no sábado"
    ]

    for mensagem in mensagens_cliente:
        time.sleep(15) 
        resposta = classificar_mensagem(mensagem, temperature=0.1)
        print(f"Cliente: {mensagem}")
        print(f"Resposta: {resposta}\n")

def testar_temperatura_unica(temp_escolhida):
    print(f"\n{'='*50}")
    print(f"=== INICIANDO TESTE: 10 Repetições | Temperatura: {temp_escolhida} ===")
    print(f"{'='*50}")
    
    repeticoes = 10
    mensagem_teste = "Preciso contestar uma cobrança indevida no meu cartão."
    sucessos = 0
    fallbacks = 0
    
    for i in range(repeticoes):
        time.sleep(15) 
        resultado = classificar_mensagem(mensagem_teste, temperature=temp_escolhida)
        
        if resultado.get("status") == "sucesso":
            sucessos += 1
            print(f"  [{i+1}/{repeticoes}] ✅ Categoria: {resultado.get('categoria')}")
        else:
            fallbacks += 1
            print(f"  [{i+1}/{repeticoes}] ❌ Fallback acionado! Erro: {resultado.get('detalhe_erro')}")
            
    taxa = (sucessos / repeticoes) * 100
    print(f"\n-> Resumo Temp {temp_escolhida}: {sucessos} Acertos | {fallbacks} Fallbacks | Taxa: {taxa}%\n")

if __name__ == "__main__":
    while True:
        print("-------------------------------------------------")
        print("ESCOLHA O QUE VOCÊ QUER TESTAR:")
        print("1 - Rodar mensagens originais (7 requests)")
        print("2 - Testar Temperatura 0.1 (10 requests)")
        print("3 - Testar Temperatura 0.7 (10 requests)")
        print("4 - Testar Temperatura 1.5 (10 requests)")
        print("0 - Sair")
        print("-------------------------------------------------")
        
        opcao = input("Digite o número da opção desejada: ")
        
        if opcao == "1":
            rodar_mensagens_originais()
        elif opcao == "2":
            testar_temperatura_unica(0.1)
        elif opcao == "3":
            testar_temperatura_unica(0.7)
        elif opcao == "4":
            testar_temperatura_unica(1.5)
        elif opcao == "0":
            print("Saindo...")
            sys.exit()
        else:
            print("Opção inválida.")
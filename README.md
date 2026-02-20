# IA Generativa

**Prof. Sabrina Bet**

Disciplina eletiva focada em conceitos e aplicações práticas de Inteligência Artificial Generativa, explorando desde integração com APIs LLM até produção de sistemas robustos.

---

## 📚 Aulas

### Aula 01 - Introdução à IA Generativa com OpenAI

**Objetivo**: Entender os fundamentos de IA Generativa e integração com APIs

**Conteúdo**:
- Conceitos fundamentais de modelos de linguagem
- Integração com OpenAI API
- Prompts efetivos
- Controle de temperatura e parâmetros
- Análise de riscos e arquitetura

**Projeto Prático** (`projeto01/`):
- Cliente OpenAI integrado
- Prompts estruturados para diferentes contextos
- Teste com modelo GPT-4o-mini

📊 [Acessar Slides](https://eletiva-aula01.lovable.app/)

---

### Aula 02 - Produção Ready: Validação e Robustez

**Objetivo**: Transformar protótipos em soluções confiáveis para produção

**Conteúdo**:
- Criação de classificadores com IA
- Validação de dados e formato JSON
- Tratamento de erros e exceções
- Testes com múltiplas execuções e temperaturas
- Implementação em ambiente de produção

**Projeto Prático** (`projeto02/`):
- Classificador de mensagens de cliente
- Parser JSON robusto
- Validação contra lista permitida
- Testes comparativos de temperatura
- Relatório de análise

**Desafio**: [Ver tarefa.md](projeto02/tarefa.md)

📊 [Acessar Slides](https://eletiva-aula02.lovable.app)

---

## 📂 Estrutura do Repositório

```
├── projeto01/          # Aula 01 - Fundamentos
│   ├── main.py         # Script principal
│   └── requirements.txt # Dependências
│
├── projeto02/          # Aula 02 - Produção
│   ├── main.py         # Classificador principal
│   ├── classifier.py   # Lógica de classificação
│   ├── llm_client.py   # Cliente LLM
│   ├── validator.py    # Validação e testes
│   ├── requirements.txt # Dependências
│   └── tarefa.md       # Desafio da aula
│
└── README.md          # Este arquivo
```

---

## 🚀 Como Começar

1. Clone ou acesse o repositório
2. Navegue até o projeto desejado
3. Instale as dependências: `pip install -r requirements.txt`
4. Configure sua chave de API OpenAI em um arquivo `.env`
5. Execute: `python main.py`

---

## 🔧 Requisitos

- Python 3.8+
- Chave de API OpenAI
- Dependências listadas em `requirements.txt`

---

## 📝 Notas Importantes

- Cada aula constrói sobre conceitos da aula anterior
- Projeto 02 foca em padrões de produção não abordados no Projeto 01
- Todos os scripts requerem autenticação OpenAI válida


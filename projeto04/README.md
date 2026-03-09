# 🤖 Logos — Chatbot com Memória (Aula 04)

## 💡 O nome: Logos

**Logos** (λόγος) é uma palavra grega que significa *palavra*, *razão* e *discurso*. Na filosofia grega antiga — especialmente em Heráclito e depois em estoicos como Marco Aurélio — Logos representava o princípio racional que governa o universo, a lógica por trás de todas as coisas. Em Aristóteles, era um dos três pilares da retórica: o argumento racional, em contraste com o *ethos* (caráter) e o *pathos* (emoção).

O nome foi escolhido porque resume o propósito do assistente: **conversar com razão**, processar linguagem com lógica e responder com clareza. Um chatbot chamado Logos carrega a ideia de que a linguagem não é apenas comunicação — é pensamento estruturado.

---

Chatbot conversacional com memória persistente, persona definida e funções utilitárias integradas, usando a API **Groq** com o modelo `llama3-70b-8192`.

---

## 🚀 Como executar

### 1. Instale as dependências

```bash
pip install groq python-dotenv
```

### 2. Configure a chave de API

Crie um arquivo `.env` na raiz do projeto:

```
GROQ_API_KEY=sua_chave_aqui
```

> Obtenha sua chave gratuita em: https://console.groq.com

### 3. Execute o chatbot

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

```
.
├── main.py          # Arquivo principal — loop do chat
├── memoria.py       # Gerenciador de histórico com persistência JSON
├── tools.py         # Funções utilitárias Python
├── historico.json   # Gerado automaticamente ao conversar
└── .env             # Chave de API (não versionar!)
```

---

## ✅ Funcionalidades Implementadas

### Parte 1 — Controle de Memória
- Comando `/limpar` apaga o histórico da conversa
- Assistente confirma com: *"Memória da conversa apagada. ✨"*

### Parte 2 — Persona do Assistente
- System prompt define o **Logos**: direto, bem-humorado, fala português do Brasil
- Todas as respostas refletem essa personalidade consistentemente

### Parte 3 — Limite de Memória
- Histórico limitado às **últimas 10 mensagens** (sem contar o system prompt)
- Mensagens mais antigas são removidas automaticamente ao ultrapassar o limite

### Parte 4 — Integração de Funções Python
Cinco funções implementadas em `tools.py`, acionadas automaticamente por detecção de intenção:

| Função | Gatilho (exemplos) |
|---|---|
| `data_atual()` | "que dia é hoje?", "qual a data atual?" |
| `calcular_idade(ano, mes, dia)` | "nasceu em 1990, quantos anos tem?" |
| `converter_temperatura(val, de, para)` | "converta 100°C para F" |
| `calcular_imc(peso, altura)` | "meu IMC com 70kg e 1.75m" |
| `gerar_senha(tamanho, especiais)` | "gera uma senha segura de 16 caracteres" |

### Parte 5 — Persistência de Dados
- Histórico salvo automaticamente em `historico.json` após cada mensagem
- Histórico carregado ao reiniciar o programa, com contagem exibida no início
- Formato JSON legível com indentação

---

## 💬 Comandos disponíveis

| Comando | Descrição |
|---|---|
| `/limpar` | Apaga o histórico de conversa |
| `/ajuda` | Exibe a lista de comandos |
| `sair` / `exit` | Encerra o programa |

---

## 🧠 Reflexões

### Se o histórico crescer muito, quais problemas podem ocorrer no uso de LLMs?

O principal problema é o **limite de contexto (context window)**: cada modelo aceita uma quantidade máxima de tokens por requisição. Um histórico muito longo pode ultrapassar esse limite, causando erros ou fazendo com que mensagens antigas sejam cortadas automaticamente pela API. Além disso, históricos grandes aumentam o **custo por requisição** (em APIs pagas) e o **tempo de resposta**, já que o modelo precisa processar mais texto. Por fim, muito contexto irrelevante pode "diluir" a atenção do modelo nas informações realmente importantes — fenômeno conhecido como *lost in the middle*.

### Por que algumas tarefas são melhores resolvidas por funções Python do que pelo próprio LLM?

LLMs são modelos probabilísticos — eles *estimam* respostas com base em padrões treinados, não *calculam* com precisão determinística. Para tarefas como cálculos matemáticos, geração de senhas aleatórias, acesso à data/hora real ou consultas a bancos de dados, funções Python são superiores porque: (1) produzem resultados **exatos e reproduzíveis**, (2) têm **acesso ao estado real do sistema** (hora atual, arquivos, APIs externas), e (3) são **mais rápidas e baratas** para esse tipo de operação do que uma chamada completa à API do LLM.

### Quais riscos existem ao deixar que o LLM tome decisões sobre quando usar uma função?

O LLM pode acionar uma função em momentos inadequados (**falsos positivos**) ou deixar de acionar quando necessário (**falsos negativos**). Em sistemas mais avançados (como *function calling* ou *agents*), o modelo pode interpretar mal os parâmetros e passar valores incorretos para a função — como extrair o ano errado de uma frase ambígua. Há também o risco de **prompt injection**: um usuário malicioso pode formular uma pergunta que engane o modelo a chamar funções com parâmetros perigosos. Por isso, toda entrada passada para funções Python deve ser validada antes da execução.

---

## 🔧 Exemplo de conversa

```
Você: que dia é hoje?
Logos: Hoje é segunda-feira, 09/06/2025. Mais alguma coisa?

Você: converta 37°C para F
Logos: 37°C equivale a 98.60°F — temperatura de corpo humano saudável!

Você: gera uma senha segura de 16 caracteres
Logos: Aqui está sua senha: aX#9mK!2pLw$3rQz

Você: /limpar
Logos: Memória da conversa apagada. ✨
```
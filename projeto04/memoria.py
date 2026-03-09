import json
import os

ARQUIVO_HISTORICO = "historico.json"
LIMITE_MENSAGENS = 10


class GerenciadorMemoria:
    def __init__(self):
        self.historico = []
        self.carregar_historico()

    def adicionar(self, role: str, content: str):
        """Adiciona mensagem ao histórico respeitando o limite."""
        self.historico.append({"role": role, "content": content})

        # Garante no máximo LIMITE_MENSAGENS (sem contar system)
        mensagens_sem_system = [m for m in self.historico if m["role"] != "system"]
        if len(mensagens_sem_system) > LIMITE_MENSAGENS:
            # Remove a mensagem mais antiga que não seja system
            for i, msg in enumerate(self.historico):
                if msg["role"] != "system":
                    self.historico.pop(i)
                    break

        self.salvar_historico()

    def limpar(self):
        """Apaga todo o histórico de conversa (mantém system prompt)."""
        self.historico = [m for m in self.historico if m["role"] == "system"]
        self.salvar_historico()

    def obter_mensagens(self) -> list:
        """Retorna o histórico completo para enviar à API."""
        return self.historico

    def salvar_historico(self):
        """Persiste o histórico em arquivo JSON."""
        try:
            with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Aviso] Não foi possível salvar histórico: {e}")

    def carregar_historico(self):
        """Carrega o histórico do arquivo JSON, se existir."""
        if os.path.exists(ARQUIVO_HISTORICO):
            try:
                with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    # Filtra apenas mensagens válidas
                    self.historico = [
                        m for m in dados
                        if isinstance(m, dict) and "role" in m and "content" in m
                    ]
                print(f"[Sistema] Histórico carregado ({len([m for m in self.historico if m['role'] != 'system'])} mensagens anteriores).")
            except Exception as e:
                print(f"[Aviso] Não foi possível carregar histórico: {e}")
                self.historico = []
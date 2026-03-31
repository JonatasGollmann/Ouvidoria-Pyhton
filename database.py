import json
import os
from manifestacao import Manifestacao, ListaEncadeada

class Database:

    def __init__(self, arquivo="manifestacoes.json"):
        self.arquivo = arquivo
        self.manifestacoes = ListaEncadeada()
        self.proximo_codigo = 1
        self._carregar_dados()

    def _carregar_dados(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    for m in dados:
                        self.manifestacoes.inserir(
                            Manifestacao(m['codigo'], m['tipo'], m['descricao'])
                        )
                    if len(self.manifestacoes) > 0:
                        self.proximo_codigo = max(m.codigo for m in self.manifestacoes) + 1
            except json.JSONDecodeError:
                self.manifestacoes = ListaEncadeada()

    def _salvar_dados(self):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            dados = [m.to_dict() for m in self.manifestacoes]
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def criar(self, tipo, descricao):
        if not descricao.strip():
            raise ValueError("Descrição não pode estar vazia")

        if tipo not in ["Elogio", "Crítica", "Comentário"]:
            raise ValueError("Tipo inválido. Use: Elogio, Crítica ou Comentário")

        nova_manifestacao = Manifestacao(self.proximo_codigo, tipo, descricao)
        self.manifestacoes.inserir(nova_manifestacao)
        self.proximo_codigo += 1
        self._salvar_dados()
        return nova_manifestacao

    def buscar_por_codigo(self, codigo):
        return self.manifestacoes.buscar_por_codigo(codigo)

    def buscar_por_tipo(self, tipo):
        return [m for m in self.manifestacoes if m.tipo == tipo]

    def buscar_por_descricao(self, palavra_chave):
        palavra_chave = palavra_chave.lower()
        return [m for m in self.manifestacoes if palavra_chave in m.descricao.lower()]

    def listar_todas(self):
        return self.manifestacoes.para_lista()

    def remover(self, codigo):
        removido = self.manifestacoes.remover(codigo)
        if removido:
            self._salvar_dados()
        return removido

    def total_manifestacoes(self):
        return len(self.manifestacoes)

    def contar_por_tipo(self):
        contagem = {"Elogio": 0, "Crítica": 0, "Comentário": 0}
        for manifestacao in self.manifestacoes:
            contagem[manifestacao.tipo] += 1
        return contagem

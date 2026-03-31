import json
import os
from manifestacao import Manifestacao

class Database:

    
    def __init__(self, arquivo="manifestacoes.json"):
        self.arquivo = arquivo
        self.manifestacoes = []
        self.proximo_codigo = 1
        self._carregar_dados()
    
    def _carregar_dados(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.manifestacoes = [
                        Manifestacao(m['codigo'], m['tipo'], m['descricao'])
                        for m in dados
                    ]
                    if self.manifestacoes:
                        self.proximo_codigo = max(m.codigo for m in self.manifestacoes) + 1
            except json.JSONDecodeError:
                self.manifestacoes = []
        else:
            self.manifestacoes = []
    
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
        self.manifestacoes.append(nova_manifestacao)
        self.proximo_codigo += 1
        self._salvar_dados()
        return nova_manifestacao
    
    def buscar_por_codigo(self, codigo):
        for manifestacao in self.manifestacoes:
            if manifestacao.codigo == codigo:
                return manifestacao
        return None
    
    def buscar_por_tipo(self, tipo):
        return [m for m in self.manifestacoes if m.tipo == tipo]
    
    def buscar_por_descricao(self, palavra_chave):
        palavra_chave = palavra_chave.lower()
        return [m for m in self.manifestacoes 
                if palavra_chave in m.descricao.lower()]
    
    def listar_todas(self):
        return self.manifestacoes.copy()
    
    def remover(self, codigo):
        for i, manifestacao in enumerate(self.manifestacoes):
            if manifestacao.codigo == codigo:
                self.manifestacoes.pop(i)
                self._salvar_dados()
                return True
        return False
    
    def total_manifestacoes(self):
        return len(self.manifestacoes)
    
    def contar_por_tipo(self):
        contagem = {"Elogio": 0, "Crítica": 0, "Comentário": 0}
        for manifestacao in self.manifestacoes:
            contagem[manifestacao.tipo] += 1
        return contagem

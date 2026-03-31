class Manifestacao:
    def __init__(self, codigo, tipo, descricao):
        self.codigo = codigo
        self.tipo = tipo
        self.descricao = descricao

    def __str__(self):
        return f"[{self.codigo}] {self.tipo}: {self.descricao}"

    def __repr__(self):
        return f"Manifestacao(codigo={self.codigo}, tipo='{self.tipo}', descricao='{self.descricao}')"

    def to_dict(self):
        return {
            'codigo': self.codigo,
            'tipo': self.tipo,
            'descricao': self.descricao
        }


class No:
    def __init__(self, manifestacao):
        self.manifestacao = manifestacao
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.cabeca = None
        self._tamanho = 0

    def inserir(self, manifestacao):
        novo_no = No(manifestacao)
        if self.cabeca is None:
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no
        self._tamanho += 1

    def remover(self, codigo):
        atual = self.cabeca
        anterior = None
        while atual is not None:
            if atual.manifestacao.codigo == codigo:
                if anterior is None:
                    self.cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                self._tamanho -= 1
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def buscar_por_codigo(self, codigo):
        atual = self.cabeca
        while atual is not None:
            if atual.manifestacao.codigo == codigo:
                return atual.manifestacao
            atual = atual.proximo
        return None

    def para_lista(self):
        resultado = []
        atual = self.cabeca
        while atual is not None:
            resultado.append(atual.manifestacao)
            atual = atual.proximo
        return resultado

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        atual = self.cabeca
        while atual is not None:
            yield atual.manifestacao
            atual = atual.proximo

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

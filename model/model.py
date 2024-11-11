
# models/musicas.py
class Musica:
    def __init__(self, nome, cantor, lancamento):
        self.nome = nome
        self.cantor = cantor
        self.lancamento = lancamento

    def to_dict(self):
        return {'nome': self.nome, 'cantor': self.cantor, 'lancamento': self.lancamento}

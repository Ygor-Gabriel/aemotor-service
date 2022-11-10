from helpers.database import db
class Passageiro_db(db.Model):
    __tablename__ = 'tb_passageiro'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cidadeOrigem = db.Column(db.String(90), nullable=False)
    cidadeDestino = db.Column(db.String(90), nullable=False)    
    
    aluno_id = db.Column(db.Integer, db.ForeignKey('tb_aluno.id_aluno'))
    aluno = db.relationship("Aluno_db")
    
    def __init__(self, aluno, cidadeOrigem, cidadeDestino):
        self.aluno = aluno
        self.cidadeOrigem = cidadeOrigem
        self.cidadeDestino = cidadeDestino

    def __repr__(self):
        return 'Aluno {}\nCidade Origem {} Cidade Destino {}\n '.format(self.aluno, self.cidadeOrigem, self.cidadeDestino)
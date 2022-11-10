from helpers.database import db
class Uf_db(db.Model):
    __tablename__ = 'tb_uf'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(90), nullable=False)
    sigla = db.Column(db.String(6), nullable=False)
    
    cidade_parent = db.Column(db.Integer, db.ForeignKey("tb_cidade.id"))
    
    def __init__(self, nome, sigla):
        self.nome = nome
        self.sigla = sigla

    def __repr__(self):
        return 'Nome {} Sigla {}\n'.format(self.nome, self.sigla)
from model.pessoa import Pessoa_db
from helpers.database import db

class Prefeito_db(Pessoa_db,db.Model):
    
    __tablename__ = 'tb_prefeito'
    __mapper_args__ = {'polymorphic_identity': 'prefeito', 'concrete': True}
    
    id_prefeito = db.Column(db.Integer, primary_key=True)
    nomePrefeito = db.Column(db.String(80), nullable=False)
    
    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id"))
    prefeitura_id = db.Column(db.Integer, db.ForeignKey("tb_prefeitura.id"))
    
    def __init__(self, pessoa):
        self.pessoa = pessoa

    def __repr__(self):
        return 'Prefeito:{}\n '.format(self.pessoa)

from model.funcionario import Funcionario_db
from helpers.database import db

class Motorista_db(Funcionario_db,db.Model):
    __tablename__ = 'tb_motorista'
    __mapper_args__ = {'polymorphic_identity': 'motorista', 'concrete': True}
    
    id = db.Column(db.Integer, primary_key=True)
    rotas = db.Column(db.String(80), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("tb_funcionario.id_fun"))
    
    veiculo_child = db.relationship('Veiculo_db',uselist=False)
    
    def __init__(self, rotas,funcionario):
        self.funcionario = funcionario
        self.rotas = rotas

    def __repr__(self):
        return 'Rotas {}\n '.format(self.rotas, self.funcionario)
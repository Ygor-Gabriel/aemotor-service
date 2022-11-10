from helpers.database import db


class Funcionario_db(db.Model):
    __tablename__ = "tb_funcionario"
    __mapper_args__ = {'polymorphic_identity': 'funcionario', 'concrete': True}
    
    id_fun = db.Column(db.Integer, primary_key=True)
    prefeitura = db.Column(db.String(90), nullable=False)
    cargo = db.Column(db.String(30), nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id"))
    
    prefeitura_id = db.Column(db.Integer, db.ForeignKey('tb_prefeitura.id'), nullable=False)
    
    motorista = db.relationship("Motorista_db", uselist=False)
    pessoa = db.relationship("Pessoa_db",foreign_keys=[pessoa_id])
    
    def __init__(self, prefeitura, cargo, pessoa):
        self.prefeitura = prefeitura
        self.cargo = cargo
        self.pessoa = pessoa

    def __repr__(self):
        return '\nPrefeitura {}\n Cargo {}\n'.format(self.prefeitura, self.cargo)

    

from helpers.database import db
from sqlalchemy.types import String


class Pessoa_db(db.Model):

    __tablename__ = "tb_pessoa"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    nascimento = db.Column(db.Date)
    email = db.Column(db.String, unique=True)
    telefone = db.Column(db.String(11))

   
    aluno_child = db.relationship("Aluno_db", uselist=False)
    prefeito_child = db.relationship("Prefeito_db", uselist=False)
    endereco_child = db.relationship("Endereco_db", uselist=False)
    funcionario_child = db.relationship("Funcionario_db", uselist=False)
    gestor_child = db.relationship("GestorApp_db", uselist=False)

    # Herança: Superclasse
    tipo_pessoa = db.Column('tipo_pessoa', String(50))
    __mapper_args__ = {'polymorphic_on': tipo_pessoa}

    def __init__(self, nome, nascimento, email, telefone):
        self.nome = nome
        self.nascimento = nascimento
        self.email = email
        self.telefone = telefone

    def __repr__(self):
        return '<Nome: {}\n Data de Nascimento: {}\n Email: {}\n Telefone: {}>'.format(self.nome, self.nascimento, self.email, self.telefone)

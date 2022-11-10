from model.pessoa import Pessoa_db
from helpers.database import db

class Aluno_db(Pessoa_db,db.Model):
    
    __tablename__ = 'tb_aluno'
    __mapper_args__ = {'polymorphic_identity': 'aluno', 'concrete': True}

    id_aluno = db.Column(db.Integer, primary_key=True)
    instituicaoDeEnsino = db.Column(db.String(80), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    matricula = db.Column(db.String(20), nullable=False)
    
    pessoa_id = db.Column(db.Integer, db.ForeignKey("tb_pessoa.id"))
    
    instituicao_child = db.relationship("InstituicaoDeEnsino_db", uselist=False)
    rotas = db.relationship('Rota_db', backref='Rota_db', lazy=True)
    passageiro_child = db.relationship('Passageiro_db',uselist=False)
    

    def __init__(self, nome, nascimento, email, telefone, instituicaoDeEnsino, curso, matricula,pessoa):
        super().__init__(nome, nascimento, email, telefone)
        self.instituicaoDeEnsino = instituicaoDeEnsino
        self.curso = curso
        self.matricula = matricula
        self.pessoa = pessoa
    
    def __repr__(self):
        return '\nNome:{}\n Nascimento: {}\n Email: {}\n Telefone: {}\n Instituto: {}\n Curso: {}\n Matrícula: {}'.format(self.nome, self.nascimento, self.email, self.telefone, self.instituicaoDeEnsino, self.curso, self.matricula)
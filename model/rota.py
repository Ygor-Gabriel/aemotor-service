from helpers.database import db

class Rota_db(db.Model):
    
    __tablename__ = 'tb_Rota'

    id = db.Column(db.Integer, primary_key=True)
    nomeDestino = db.Column(db.String(30), nullable=False)
    qtdalunos = db.Column(db.String(11), nullable=False)
    prefeitura = db.Column(db.String(80), nullable=False)
    veiculo = db.Column(db.String(30), nullable=False)
    passageiro = db.Column(db.String(11), nullable=False)
    horaSaida = db.Column(db.String(80), nullable=False)
    horaChegada = db.Column(db.String(80), nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('tb_aluno.id_aluno'), nullable=False)
  
    prefeitura_child = db.relationship("Prefeitura_db", uselist=False)
    instituicoes = db.relationship('InstituicaoDeEnsino_db', backref='InstituicaoDeEnsino_db', lazy=True)
   
    def __init__(self, nomeDestino, qtdalunos, prefeitura, veiculo, passageiro, horaSaida, horaChegada):
        self.nomeDestino = nomeDestino
        self.qtdalunos = qtdalunos
        self.prefeitura = prefeitura        
        self.veiculo = veiculo
        self.passageiro = passageiro
        self.horaSaida = horaSaida
        self.horaChegada = horaChegada

    def __repr__(self):
        return 'Nome destino {}  Quantidade de Alunos {} Prefeitura {} Veiculo {} Passageiro {} Hora de Saída {} Hora de chegada {}\n'.format(self.nomeDestino, self.qtdalunos, self.prefeitura, self.veiculo, self.passageiro, self.horaSaida, self.horaChegada)
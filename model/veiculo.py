from helpers.database import db
class Veiculo_db(db.Model):
    __tablename__ = 'tb_veiculo'

    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(80), nullable=False)
    qtdPassageiros = db.Column(db.String(10), nullable=False)
    tipoVeiculo = db.Column(db.String(20), nullable=False)
    placa = db.Column(db.String(20), nullable=False)
    motorista_id = db.Column(db.Integer, db.ForeignKey("tb_motorista.id"))
    
    
    def __init__(self, cidade, qtdPassageiros, tipoVeiculo, placa,motorista):
        self.cidade = cidade
        self.qtdPassageiros = qtdPassageiros
        self.tipoVeiculo = tipoVeiculo
        self.placa = placa
        self.motorista = motorista

    def __repr__(self):
        return 'Cidade: {} Quantidade de passageiros: {} Tipo do veículo: {} Placa: {}\n'.format(self.cidade, self.qtdPassageiros, self.tipoVeiculo, self.placa)
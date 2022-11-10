from model.rota import Rota_db
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('nomeDestino', required=True)
parser.add_argument('qtdalunos', required=True)
parser.add_argument('prefeitura', required=True)
parser.add_argument('veiculo', required=True)
parser.add_argument('passageiro', required=True)
parser.add_argument('horaSaida', required=True)
parser.add_argument('horaChegada', required=True)


class Rota(Resource):
    def get(self):
        current_app.logger.info("Get - Rota")
        rota = Rota_db.query\
            .order_by(Rota_db.nomeDestino)\
            .all()
        return rota, 200
    
    def post(self):
        current_app.logger.info("Post - Rotas")
        try:
            # JSON
            args = parser.parse_args()
            nomeDestino = args['nomeDestino']
            qtdalunos = args['qtdalunos']
            veiculo = args['veiculo']
            passageiro = args['passageiro']
            horaSaida = args['horaSaida']
            horaChegada = args['horaChegada']
            
            # Rota
            rota = Rota_db(nomeDestino,qtdalunos,passageiro,veiculo,horaSaida,horaChegada)
            # Criação do Rota.
            db.session.add(rota)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, rota_id):
        current_app.logger.info("Put - Rotas")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Rotas: %s:" % args)
            # Evento
            nomeDestino = args['nomeDestino']
            qtdalunos = args['qtdalunos']
            veiculo = args['veiculo']
            passageiro = args['passageiro']
            horaSaida = args['horaSaida']
            horaChegada = args['horaChegada']
            
            Rota_db.query \
                .filter_by(id=rota_id) \
                .update(dict(nomeDestino=nomeDestino,qtdalunos = qtdalunos, veiculo = veiculo,passageiro = passageiro,horaSaida = horaSaida,horaChegada = horaChegada))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, rota_id):
        current_app.logger.info("Delete - Rotas: %s:" % rota_id)
        try:
            Rota_db.query.filter_by(id=rota_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
    
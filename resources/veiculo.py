from model.veiculo import Veiculo_db
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('cidade', required=True)
parser.add_argument('qtdPassageiros', required=True)
parser.add_argument('tipoVeiculo', required=True)
parser.add_argument('placa', required=True)

class Veiculo(Resource):
    def get(self):
        current_app.logger.info("Get - Veiculo")
        veiculo = Veiculo_db.query\
            .order_by(Veiculo_db.cidade)\
            .all()
        return veiculo, 200
    def post(self):
        current_app.logger.info("Post - Veiculos")
        try:
            # JSON
            args = parser.parse_args()
            cidade = args['cidade']
            qtdPassageiros = args['qtdPassageiros']
            tipoVeiculo = args['tipoVeiculo']
            placa = args['placa']
            # Veiculo
            veiculo = Veiculo_db(cidade,qtdPassageiros,tipoVeiculo,placa)
            # Criação do Veiculo.
            db.session.add(veiculo)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, veiculo_id):
        current_app.logger.info("Put - Veiculos")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Veiculos: %s:" % args)
            # Evento
            cidade = args['cidade']
            qtdPassageiros = args['qtdPassageiros']
            tipoVeiculo = args['tipoVeiculo']
            placa = args['placa']
            
            Veiculo_db.query \
                .filter_by(id=veiculo_id) \
                .update(dict(cidade=cidade,qtdPassageiros = qtdPassageiros, tipoVeiculo = tipoVeiculo,placa = placa))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, veiculo_id):
        current_app.logger.info("Delete - Veiculos: %s:" % veiculo_id)
        try:
            Veiculo_db.query.filter_by(id=veiculo_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
    
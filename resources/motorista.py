from model.motorista import Motorista_db
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal


parser = reqparse.RequestParser()
parser.add_argument('rotas', required=True)


class Motorista(Resource):
    def get(self):
        current_app.logger.info("Get - Motorista")
        motorista = Motorista_db.query\
            .order_by(Motorista_db.rotas)\
            .all()
        return motorista, 200
    def post(self):
        current_app.logger.info("Post - Motoristas")
        try:
            # JSON
            args = parser.parse_args()
            rotas = args['rotas']
           
            # Motorista
            motorista = Motorista_db(rotas)
            # Criação do Motorista.
            db.session.add(motorista)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, motorista_id):
        current_app.logger.info("Put - Motoristas")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Funcionario: %s:" % args)
            # Evento
            prefeitura = args['prefeitura']
            cargo = args['cargo']
    

            Motorista_db.query \
                .filter_by(id=motorista_id) \
                .update(dict(prefeitura=prefeitura,cargo = cargo ))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, motorista_id):
        current_app.logger.info("Delete - Motoristas: %s:" % motorista_id)
        try:
            Motorista_db.query.filter_by(id=motorista_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
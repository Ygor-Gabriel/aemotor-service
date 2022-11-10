from flask import jsonify
from model.error import Error, error_campos
from sqlalchemy import exc
from helpers.database import db
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal
from model.prefeitura import Prefeitura_db

parser = reqparse.RequestParser()
parser.add_argument('email', required=True)

class Prefeitura(Resource):
    def get(self):
        current_app.logger.info("Get - Prefeituras ")
        prefeitura = Prefeitura_db.query\
            .order_by(Prefeitura_db.email)\
            .all()
        return prefeitura, 200
    
    def post(self):
        current_app.logger.info("Post - Prefeitura")
        try:
            # JSON
            args = parser.parse_args()
            email = args['email']

            # Prefeitura
            prefeitura = Prefeitura_db(email)
            # Criação do Prefeitura.
            db.session.add(prefeitura)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, prefeitura_id):
        current_app.logger.info("Put - Prefeitura")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Prefeitura: %s:" % args)
            # Evento
            email = args['email']

            Prefeitura_db.query \
                .filter_by(id=prefeitura_id) \
                .update(dict(email=email))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, prefeitura_id):
        current_app.logger.info("Delete - Prefeitura: %s:" % prefeitura_id)
        try:
            Prefeitura_db.query.filter_by(id=prefeitura_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
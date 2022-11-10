from model.prefeito import Prefeito_db
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)

class Prefeito(Resource):
    def get(self):
        current_app.logger.info("Get - Prefeitos")
        prefeito = Prefeito_db.query\
            .order_by(Prefeito_db.nome)\
            .all()
        return prefeito, 200
    def post(self):
        current_app.logger.info("Post - Prefeitos")
        try:
            # JSON
            args = parser.parse_args()
            nome = args['nome']
          

            # Prefeito
            prefeito = Prefeito_db(nome)
            # Criação do Prefeito.
            db.session.add(prefeito)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, prefeito_id):
        current_app.logger.info("Put - Prefeitos")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Prefeitos: %s:" % args)
            # Evento
            nome = args['nome']
            
    

            Prefeito_db.query \
                .filter_by(id=prefeito_id) \
                .update(dict(nome=nome ))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, prefeito_id):
        current_app.logger.info("Delete - Prefeitos: %s:" % prefeito_id)
        try:
            Prefeito_db.query.filter_by(id=prefeito_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
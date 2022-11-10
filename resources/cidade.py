from model.cidade import Cidade_db
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('sigla', required=True)


class Cidade(Resource):
    def get(self):
        current_app.logger.info("Get - Cidades")
        cidade = Cidade_db.query\
            .order_by(Cidade_db.sigla)\
            .all()
        return cidade, 200
    def post(self):
        current_app.logger.info("Post - Cidades")
        try:
            # JSON
            args = parser.parse_args()
            nome = args['nome']
            sigla = args['sigla']

            # Cidade
            cidade = Cidade_db(nome,sigla)
            # Criação do Cidade.
            db.session.add(cidade)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, cidade_id):
        current_app.logger.info("Put - Cidades")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Cidade: %s:" % args)
            # Evento
            nome = args['nome']
            sigla = args['sigla']
    

            Cidade_db.query \
                .filter_by(id=cidade_id) \
                .update(dict(nome=nome,sigla = sigla ))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, cidade_id):
        current_app.logger.info("Delete - Cidades: %s:" % cidade_id)
        try:
            Cidade_db.query.filter_by(id=cidade_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
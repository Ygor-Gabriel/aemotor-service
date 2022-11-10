from model.pessoa import Pessoa_db
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('nascimento', required=True)
parser.add_argument('email', required=True)
parser.add_argument('telefone', required=True)




class Pessoa(Resource):
    def get(self):
        current_app.logger.info("Get - Pessoas ")
        pessoa = Pessoa_db.query\
            .order_by(Pessoa_db.email)\
            .all()
        return pessoa, 200
    def post(self):
        current_app.logger.info("Post - Pessoas")
        try:
            # JSON
            args = parser.parse_args()
            nome = args['nome']
            nascimento = args['nascimento']
            email = args['email']
            telefone = args['telefone']
            # Pessoa
            pessoa = Pessoa_db(nome,nascimento,email,telefone)
            # Criação do Pessoa.
            db.session.add(pessoa)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, pessoa_id):
        current_app.logger.info("Put - Pessoas")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Pessoa: %s:" % args)
            # Evento
            nome = args['nome']
            nascimento = args['nascimento']
            email = args['email']
            telefone = args['telefone']

            Pessoa_db.query \
                .filter_by(id=pessoa_id) \
                .update(dict(nome=nome,nascimento = nascimento, email = email, telefone = telefone))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, pessoa_id):
        current_app.logger.info("Delete - Pessoas: %s:" % pessoa_id)
        try:
            Pessoa_db.query.filter_by(id=pessoa_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
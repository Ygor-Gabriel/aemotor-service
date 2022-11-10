from model.instituicaoEnsino import InstituicaoDeEnsino
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('telefone', required=True)
parser.add_argument('logradouro', required=True)

class InstituicaoDeEnsino(Resource):
    def get(self):
        current_app.logger.info("Get - InstituicaoDeEnsino")
        instituicao = InstituicaoDeEnsino.query\
            .order_by(InstituicaoDeEnsino.nome)\
            .all()
        return instituicao, 200
    def post(self):
        current_app.logger.info("Post - InstituicaoDeEnsino")
        try:
            # JSON
            args = parser.parse_args()
            nome = args['nome']
            telefone = args['telefone']
            logradouro = args['logradouro']

            # Endereco
            instituicaoDeEnsino = InstituicaoDeEnsino(nome,telefone,logradouro)
            # Criação do Endereco.
            db.session.add(instituicaoDeEnsino)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, instituicao_id):
        current_app.logger.info("Put - InstituicaoDeEnsino")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("InstituicaoDeEnsino: %s:" % args)
            # Evento
            nome = args['nome']
            telefone = args['telefone']
            logradouro = args['logradouro']

            InstituicaoDeEnsino.query \
                .filter_by(id=instituicao_id) \
                .update(dict(nome=nome,telefone = telefone,logradouro=logradouro ))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, instituicao_id):
        current_app.logger.info("Delete - InstituicaoDeEnsino: %s:" % instituicao_id)
        try:
            InstituicaoDeEnsino.query.filter_by(id=instituicao_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
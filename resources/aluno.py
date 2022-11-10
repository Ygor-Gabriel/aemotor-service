from model.aluno import Aluno_db
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('instituicaoDeEnsino', required=True)
parser.add_argument('curso', required=True)
parser.add_argument('matricula', required=True)

class Aluno(Resource):
    def get(self):
        current_app.logger.info("Get - Alunodb")
        aluno = Aluno_db.query\
            .order_by(Aluno_db.curso)\
            .all()
        return aluno, 200
    
    def post(self):
        current_app.logger.info("Post - Alunos")
        try:
            # JSON
            args = parser.parse_args()
            instituicaoDeEnsino = args['instituicaoDeEnsino']
            curso = args['curso']
            matricula = args['matricula']
            # Alunodb
            aluno = Aluno_db(instituicaoDeEnsino,curso,matricula)
            # Criação do Alunodb.
            db.session.add(aluno)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, aluno_id):
        current_app.logger.info("Put - Alunos")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Alunodb: %s:" % args)
            # Evento
            instituicaoDeEnsino = args['instituicaoDeEnsino']
            curso = args['curso']
            matricula = args['matricula']

            Aluno_db.query \
                .filter_by(id=aluno_id) \
                .update(dict(instituicaoDeEnsino=instituicaoDeEnsino,curso = curso, matricula = matricula))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, aluno_id):
        current_app.logger.info("Delete - Alunodb: %s:" % aluno_id)
        try:
            Aluno_db.query.filter_by(id=aluno_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
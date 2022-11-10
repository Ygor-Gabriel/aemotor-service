from model.funcionario import Funcionario_db 
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('prefeitura', required=True)
parser.add_argument('cargo', required=True)


class Funcionario(Resource):
    def get(self):
        current_app.logger.info("Get - Funcionarios")
        funcionario = Funcionario_db.query\
            .order_by(Funcionario_db.cargo)\
            .all()
        return funcionario, 200
    def post(self):
        current_app.logger.info("Post - Funcionarios")
        try:
            # JSON
            args = parser.parse_args()
            prefeitura = args['prefeitura']
            cargo = args['cargo']

            # Funcionario
            funcionario = Funcionario_db(prefeitura,cargo)
            # Criação do Funcionario.
            db.session.add(funcionario)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, funcionario_id):
        current_app.logger.info("Put - Funcionarios")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Funcionario: %s:" % args)
            # Evento
            prefeitura = args['prefeitura']
            cargo = args['cargo']
    

            Funcionario_db.query \
                .filter_by(id=funcionario_id) \
                .update(dict(prefeitura=prefeitura,cargo = cargo ))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, funcionario_id):
        current_app.logger.info("Delete - Funcionarios: %s:" % funcionario_id)
        try:
            Funcionario_db.query.filter_by(id=funcionario_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
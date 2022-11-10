from model.uf import Uf_db
from model.error import Error, error_campos
from sqlalchemy import exc
from helpers.database import db
from flask import jsonify
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal


parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('sigla', required=True)

class Uf(Resource):
    def get(self):
        current_app.logger.info("Get - Ufs")
        uf = Uf_db.query\
            .order_by(Uf_db.sigla)\
            .all()
        return uf, 200
        
    def post(self):
        current_app.logger.info("Post - Ufs")
        try:
            # JSON
            
            args = parser.parse_args()
            sigla = args['sigla']
            nome = args['nome']
            

            # Uf
            uf = Uf_db(sigla,nome)
            # Criação do Uf.
            db.session.add(uf)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, uf_id):
        current_app.logger.info("Put - Ufs")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Ufs: %s:" % args)
            # Evento
            sigla = args['sigla']
            nome = args['nome']
           

            Uf_db.query \
                .filter_by(id=uf_id) \
                .update(dict(sigla=sigla,nome=nome))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, uf_id):
        current_app.logger.info("Delete - Ufs: %s:" % uf_id)
        try:
            Uf_db.query.filter_by(id=uf_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
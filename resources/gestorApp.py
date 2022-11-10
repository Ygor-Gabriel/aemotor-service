from model.gestorApp import GestorApp_db
from model.error import Error, error_campos
from helpers.database import db
from flask import jsonify
from sqlalchemy import exc
from flask_restful import Resource, marshal_with, reqparse, current_app, marshal

parser = reqparse.RequestParser()
parser.add_argument('admin', required=True)
class GestorApp(Resource):
    def get(self):
        current_app.logger.info("Get - GestorApp")
        gestor = GestorApp_db.query\
            .order_by(GestorApp_db.admin)\
            .all()
        return gestor, 200
    def post(self):
        current_app.logger.info("Post - GestorApp")
        try:
            # JSON
            args = parser.parse_args()
            admin = args['admin']

            # GestorApp
            gestorApp = GestorApp_db(admin)
            # Criação do GestorApp.
            db.session.add(gestorApp)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return 204
    
    def put(self, gestorApp_id):
        current_app.logger.info("Put - GestorApp")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("GestorApp: %s:" % args)
            # Evento
            admin = args['admin']
            
    

            GestorApp_db.query \
                .filter_by(id=gestorApp_id) \
                .update(dict(admin=admin))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204
    
    def delete(self, gestorApp_id):
        current_app.logger.info("Delete - GestorApp: %s:" % gestorApp_id)
        try:
            GestorApp_db.query.filter_by(id=gestorApp_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204
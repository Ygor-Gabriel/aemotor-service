from flask_restful import Resource


class IndexResource(Resource):
    def get(self):
        return {'nome': 'AeMotor', 'versao': '1.0'}
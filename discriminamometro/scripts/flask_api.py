from flask import Flask
from werkzeug.utils import cached_property
from flask_restplus import Api, Resource
from flask import request
import Discrim.api as api

app = Flask(__name__)
api = Api(app)
ns = api.namespace('Disciminamometro',
                   description='Predicciones de discriminación')



@ns.route('/Usuario', endpoint='endpoint_discriminacion_usuario')
class Modelo(Resource):
    """
    Aquí debe ir la descripción de la clase Modelo
    Aquí debe ir el segundo renglón
    Y aquí debe ir el tercer renglón
    """
    parser = ns.parser()
    parser.add_argument('usuario', required=True, type=str, help='Usuario de twitter', nullable=False)

    @ns.expect(parser, validate=True)
    def get(self):
        usuario = str(request.args.get('usuario'))
        obj_api = api.API()
        resultado = obj_api.clasificar_x_usuario('@' + usuario)
        return resultado

@ns.route('/hashtag', endpoint='endpoint_discriminacion_hashtag')
class Modelo(Resource):
    """
    Aquí debe ir la descripción de la clase Modelo
    Aquí debe ir el segundo renglón
    Y aquí debe ir el tercer renglón
    """
    parser = ns.parser()
    parser.add_argument('hashtag', required=True, type=str, help='hashtag (#) a buscar', nullable=False)

    @ns.expect(parser, validate=True)
    def get(self):
        hashtag = str(request.args.get('hashtag'))
        obj_api = api.API()
        resultado = obj_api.clasificar_x_ht('#'+hashtag)
        return resultado

@ns.route('/texto', endpoint='endpoint_discriminacion_texto')
class Modelo(Resource):
    """
    Aquí debe ir la descripción de la clase Modelo
    Aquí debe ir el segundo renglón
    Y aquí debe ir el tercer renglón
    """
    parser = ns.parser()
    parser.add_argument('texto', required=True, type=str, help='texto que se desea evaluar', nullable=False)

    @ns.expect(parser, validate=True)
    def get(self):
        texto = str(request.args.get('texto'))
        obj_api = api.API()
        resultado = obj_api.clasificar_x_texto(texto)
        return resultado

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug = False)
    #app.run()

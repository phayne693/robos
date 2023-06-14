from flask import Flask, request
from flask_restful import Resource, Api
from pix import robo_pix

app = Flask(__name__)
api = Api(app)

class Robopix(Resource):
    def post(self):
        #obtem as variaveis do payload
        chave_cpf = request.json.get('chave_cpf')
        valor = request.json.get('valor')
        #resultado pega o return da funcao robo
        resultado = robo_pix(chave_cpf, valor)
        #retorna o resultado na API
        if resultado == 'Pix realizado!':
            return {'success' : True, 'message' :resultado }, 200
        else:
            return {'success' : False, 'message' : resultado }, 500

api.add_resource(Robopix, '/robo-pix')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
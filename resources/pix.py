from flask_restful import Resource
from flask import request
from pix_cpf import robo_pix
from pix_copy_cola import pix_copia_cola

class Pix_cpf(Resource):
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

class PiX_copy_cola(Resource):
    def post(self):
        chave_copia_cola= request.json.get("chave_copia_cola")
        resutlado = pix_copia_cola(chave_copia_cola)
        if resutlado == 'Pix copia e cola realizado!':
            return {'success': True, 'message': resutlado}, 200
        else:
            return {'success': True, 'message': resutlado}, 500

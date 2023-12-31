from flask_restful import Resource
from flask import request
from robos.pix_cpf import robo_pix
from robos.pix_copy_cola import pix_copia_cola

class Pix_cpf(Resource):
    def post(self):
        #obtem as variaveis do payload
        chave_cpf = request.json.get('chave_cpf')
        valor = request.json.get('valor')
        #valida o tamanho das variaveis
        if len(chave_cpf) > 11:
            return {'success': False, 'message': 'Chave CPF deve ter no maximo 11 numeros'}, 400
        elif not chave_cpf.isnumeric():
            return {'success': False, 'message': 'CPF deve conter apenas numeros'}, 400
        #resultado pega o return da funcao robo
        resultado = robo_pix(chave_cpf, valor)
        #retorna o resultado na API
        if resultado == 'Pix realizado!':
            return {'success' : True, 'message' :resultado }, 200
        elif resultado != 'Pix realizado!':
            return {'success' : False, 'message' : resultado }, 500
        

class PiX_copy_cola(Resource):
    def post(self):
        chave_copia_cola= request.json.get("chave_copia_cola")
        resutlado = pix_copia_cola(chave_copia_cola)
        if resutlado == 'Pix copia e cola realizado!':
            return {'success': True, 'message': resutlado}, 200
        else:
            return {'success': False, 'message': resutlado}, 500


class Pix_cpf_modelo:
    def __init__(self,chave_cpf, valor):
        self.chave_cpf = chave_cpf
        self.valor = valor
    
    def json(self):
        return{
            'chave_cpf': self.chave_cpf,
            'valor': self.valor
        }
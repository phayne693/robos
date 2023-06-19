from flask import Flask
from flask_restful import Api
from resources.pix import Pix_cpf, PiX_copy_cola


app = Flask(__name__)
api = Api(app)

api.add_resource(Pix_cpf, '/pix-cpf')
api.add_resource(PiX_copy_cola, '/pix-copy-cola')

if __name__ == '__main__':
    app.run(debug=True)
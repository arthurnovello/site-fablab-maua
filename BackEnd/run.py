from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
UPLOAD_FOLDER = '/Users/lucasmarques/Downloads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

import views
import models
import resources


api.add_resource(resources.Pedido, '/Pedido/')
api.add_resource(resources.Curso, '/Curso/')
api.add_resource(resources.Solicitante, '/Solicitante/')
api.add_resource(resources.Solicitacao, '/Solicitacao/')
api.add_resource(resources.Pessoa, '/Pessoa/')
api.add_resource(resources.Sala, '/Sala/')
api.add_resource(resources.Status, '/Status/')
api.add_resource(resources.Upload, '/Upload')
api.add_resource(resources.SlackResponse, '/SlackResponse')

if __name__ == "__main__":
    app.run(debug=False)


from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)
# app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# jwt = JWTManager(app)

# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


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

if __name__ == "__main__":
    app.run(debug=False)
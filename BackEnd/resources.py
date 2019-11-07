from flask_restful import Resource, reqparse
from flask import request
from models import *
# from flask_jwt_extended import jwt_required
parser = reqparse.RequestParser()

class Pedido(Resource):
    # @jwt_required
    def post(self):
       try:
           pedido = request.get_json(force=True) 
           novo_pedido = PedidoModel(**pedido)
           novo_pedido.save_to_db()
           return {'message': 'Pedido criado com sucesso.'}, 201
       except:
           return {'message': 'Erro ao criar pedido.'}, 500
    
    # @jwt_required
    def get(self,email):
       return PedidoModel.return_by_email(email)
     
    # @jwt_required
    def delete(self, id):
       return PedidoModel.delete_by_id(id)

class Curso(Resource):
    # @jwt_required
    def post(self):
       parametro = request.get_json(force=True)
       nomeCurso = parametro.get('curso')
       novo_curso = CursoModel(curso=nomeCurso)
       try:
           novo_curso.save_to_db()
           return {'message': 'Curso criado com sucesso.'}, 201
       except:
           return {'message': 'Erro ao criar curso.'}, 500
    
    # @jwt_required
    def get(self):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return CursoModel.return_by_id(id)

    # @jwt_required
    def delete(self):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       try:
           CursoModel.delete_by_id(id)
           return {'message': 'Curso deletado com sucesso.'}, 200
       except:
           return {'message': 'Erro ao deletar curso.'}, 500

class Pessoa(Resource):
    # @jwt_required
    def post(self):
       parametro = request.get_json(force=True)
       nome = parametro.get('nome')
       email = parametro.get('email')
       ra = parametro.get('ra')
       nova_pessoa = PessoaModel(nome=nome,email=email,ra=ra)
       try:
           nova_pessoa.save_to_db()
           return {'message': 'Pessoa adicionada com sucesso.'}, 201
       except:
           return {'message': 'Erro ao adicionar pessoa.'}, 500
    
    # @jwt_required
    def get(self):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return PessoaModel.return_by_id(id)
       
     
    # @jwt_required
    def delete(self, id):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return PessoaModel.delete_by_id(id)
       
class Sala(Resource):
    # @jwt_required
    def post(self):
       parametro = request.get_json(force=True)
       nomeSala = parametro.get('sala')
       nova_sala = SalaModel(sala=nomeSala)
       try:
           nova_sala.save_to_db()
           return {'message': 'Sala adicionada com sucesso.'}, 201
       except:
           return {'message': 'Erro ao adicionar sala.'}, 500
    
    # @jwt_required
    def get(self):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return SalaModel.return_by_id(id)
       
     
    # @jwt_required
    def delete(self, id):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return SalaModel.delete_by_id(id)

class Status(Resource):
    # @jwt_required
    def post(self):
       parametro = request.get_json(force=True)
       nomeStatus = parametro.get('curso')
       novo_curso = CursoModel(curso=nomeStatus)
       try:
           novo_curso.save_to_db()
           return {'message': 'Curso criado com sucesso.'}, 201
       except:
           return {'message': 'Erro ao criar curso.'}, 500
    
    # @jwt_required
    def get(self):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return StatusModel.return_by_id(id)
       
     
    # @jwt_required
    def delete(self, id):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return StatusModel.delete_by_id(id)
    
class Solicitante(Resource):
    # @jwt_required
    def post(self):
       parametro = request.get_json(force=True)
       nomeCurso = parametro.get('curso')
       novo_curso = CursoModel(curso=nomeCurso)
       try:
           novo_curso.save_to_db()
           return {
               'message': 'Curso criado com sucesso.'
           }
       except:
           return {'message': 'Erro ao criar curso.'}, 500
    
    # @jwt_required
    def get(self):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return SolicitanteModel.return_by_id(id)
       
     
    # @jwt_required
    def delete(self, id):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return SolicitanteModel.delete_by_id(id)

class Solicitacao(Resource):
    # @jwt_required
    def post(self):
       parametro = request.get_json(force=True)
       nomeCurso = parametro.get('curso')
       novo_curso = CursoModel(curso=nomeCurso)
       try:
           novo_curso.save_to_db()
           return {
               'message': 'Curso criado com sucesso.'
           }
       except:
           return {'message': 'Erro ao criar curso.'}, 500
    
    # @jwt_required
    def get(self):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return SolicitacaoModel.return_by_id(id)
       
     
    # @jwt_required
    def delete(self, id):
       parametro = request.get_json(force=True)
       id = parametro.get('id')
       return SolicitacaoModel.delete_by_id(id)
    
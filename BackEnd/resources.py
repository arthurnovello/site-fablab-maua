from flask_restful import Resource, reqparse
from flask import request, jsonify
import slack
import os
from models import CursoModel, PedidoModel, PessoaModel, SalaModel, \
                    SolicitacaoModel, SolicitanteModel, StatusModel
from werkzeug.utils import secure_filename
from run import app
# from flask_jwt_extended import jwt_required

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
parser = reqparse.RequestParser()


class Upload(Resource):

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
            ALLOWED_EXTENSIONS

    def post(self):
        # check if the post request has the file part
        if 'files[]' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        files = request.files.getlist('files[]')

        errors = {}
        success = False

        for file in files:
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'

        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 206
            return resp
        if success:
            resp = jsonify({'message': 'Files successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp


class Pedido(Resource):
    # @jwt_required
    def post(self):
        parametro = request.get_json(force=True)
        email = parametro.get('email')
        nome = parametro.get('nome')
        if nome is None:
            pedidofiltro = PedidoModel.return_by_email(email)
            pedidofiltro["Status"] = []
            qtd = len(pedidofiltro['Pedidos'])
            array = []
            i = 0
            while i < qtd:
                array.append(pedidofiltro['Pedidos'][i].get('id'))
                i = i+1
            for k in array:
                u = StatusModel.return_by_id_pedido(k)
                if u["Status"] is None:
                    pedidofiltro["Status"].append(None)
                else:
                    pedidofiltro["Status"].append(u["Status"][0])
            #    print(u['Status'])
        #    idfiltro = pedidofiltro['Pedidos'][len(
        #       pedidofiltro['Pedidos'])-1].get('id')
        #    pedido = PedidoModel.return_by_id(idfiltro)
        #    status = StatusModel.return_by_id_pedido(idfiltro)
        #    print(u['Status'])
        #    pedido['Status'] = status['Status']
            return pedidofiltro
        else:
            verificacao = PessoaModel.return_by_email(email)
            try:
                verificacao = verificacao['Pessoa'][0]
                id_pessoa = verificacao.get('id')
            except Exception as e:
                nome = parametro.get('nome')
                ra = parametro.get('ra')
                nova_pessoa = PessoaModel(nome=nome, email=email, ra=ra)
                nova_pessoa.save_to_db()
                verificacao2 = PessoaModel.return_by_email(email)
                verificacao2 = verificacao2['Pessoa'][0]
                id_pessoa = verificacao2.get('id')
                return e

            id_solicitante = parametro.get('id_solicitante')
            id_sala = parametro.get('id_sala')
            id_curso = parametro.get('id_curso')
            id_solicitacao = parametro.get('id_solicitacao')
            data = parametro.get('data')
            duracao = parametro.get('duracao')
            qtd_pessoas = parametro.get('qtd_pessoas')
            # aprovado = parametro.get('aprovado')
            prazo = parametro.get('prazo')
            descricao = parametro.get('descricao')
            material_proprio = parametro.get('material_proprio')
            if material_proprio == "on":
                material_proprio = True
            else:
                material_proprio = False
            # material_proprio = False
            novo_pedido = PedidoModel(
                id_pessoa=id_pessoa,
                id_solicitante=id_solicitante,
                id_sala=id_sala,
                id_curso=id_curso,
                id_solicitacao=id_solicitacao,
                data=data,
                duracao=duracao,
                qtd_pessoas=qtd_pessoas,
                prazo=prazo,
                descricao=descricao,
                material_proprio=material_proprio
            )
            try:
                id_pedido = novo_pedido.save_to_db()
                novo_status = StatusModel(id_pedido=id_pedido)
                novo_status.save_to_db()
                slack.send_alert(id_pedido)
                return {'message': 'Pedido criado com sucesso.'}, 201
            except Exception as e:
                return {'message': 'Erro ao criar pedido.' + str(e)}, 500

    # @jwt_required
    def get(self):
        parametro = request.get_json(force=True)
        email = parametro.get('email')
        return PedidoModel.return_by_email(email)

    # @jwt_required
    def delete(self):
        parametro = request.get_json(force=True)
        id = parametro.get('id')
        try:
            PedidoModel.delete_by_id(id)
            return {'message': 'Pedido deletado com sucesso.'}, 200
        except Exception as e:
            return {'message': 'Erro ao deletar pedido.' + e}, 500


class Curso(Resource):
    # @jwt_required
    def post(self):
        parametro = request.get_json(force=True)
        nomeCurso = parametro.get('curso')
        novo_curso = CursoModel(curso=nomeCurso)
        try:
            novo_curso.save_to_db()
            return {'message': 'Curso criado com sucesso.'}, 201
        except Exception as e:
            return {'message': 'Erro ao criar curso.' + e}, 500

    # @jwt_required
    def get(self):
        # parametro = request.get_json(force=True)
        # id = parametro.get('id')
        # return CursoModel.return_by_id(id)
        return CursoModel.return_all()

    # @jwt_required
    def delete(self):
        parametro = request.get_json(force=True)
        id = parametro.get('id')
        try:
            CursoModel.delete_by_id(id)
            return {'message': 'Curso deletado com sucesso.'}, 200
        except Exception as e:
            return {'message': 'Erro ao deletar curso.' + e}, 500


class Pessoa(Resource):
    # @jwt_required
    def post(self):
        parametro = request.get_json(force=True)
        nome = parametro.get('nome')
        email = parametro.get('email')
        ra = parametro.get('ra')
        if (nome is None):
            return PessoaModel.return_by_email(email)
        else:
            try:
                nova_pessoa = PessoaModel(nome=nome, email=email, ra=ra)
                nova_pessoa.save_to_db()
                return {'message': 'Pessoa adicionada com sucesso.'}, 201
            except Exception as e:
                return {'message': 'Erro ao adicionar pessoa.' + e}, 500

    # @jwt_required
    def get(self):
        parametro = request.get_json(force=True)
        email = parametro.get('email')
        return PessoaModel.return_by_email(email)

    # @jwt_required
    def delete(self):
        parametro = request.get_json(force=True)
        id = parametro.get('id')
        try:
            PessoaModel.delete_by_id(id)
            return {'message': 'Pessoa deletada com sucesso.'}, 200
        except Exception as e:
            return {'message': 'Erro ao deletar pessoa.' + e}, 500


class Sala(Resource):
    # @jwt_required
    def post(self):
        parametro = request.get_json(force=True)
        nomeSala = parametro.get('sala')
        nova_sala = SalaModel(sala=nomeSala)
        try:
            nova_sala.save_to_db()
            return {'message': 'Sala adicionada com sucesso.'}, 201
        except Exception as e:
            return {'message': 'Erro ao adicionar sala.' + e}, 500

    # @jwt_required
    def get(self):
        # parametro = request.get_json(force=True)
        # id = parametro.get('id')
        # return SalaModel.return_by_id(id)
        return SalaModel.return_all()

    # @jwt_required
    def delete(self):
        parametro = request.get_json(force=True)
        id = parametro.get('id')
        try:
            SalaModel.delete_by_id(id)
            return {'message': 'Sala deletada com sucesso.'}, 200
        except Exception as e:
            return {'message': 'Erro ao deletar sala.' + e}, 500


class Status(Resource):
    # @jwt_required
    def post(self):
        parametro = request.get_json(force=True)
        id_pedido = parametro.get('id_pedido')
        termino = parametro.get('termino')
        massa = parametro.get('massa')
        tempo = parametro.get('tempo')
        concluido = parametro.get('concluido')
        novo_curso = StatusModel(
            id_pedido=id_pedido, termino=termino, massa=massa, tempo=tempo,
            concluido=concluido)
        try:
            novo_curso.save_to_db()
            return {'message': 'Status criado com sucesso.'}, 201
        except Exception as e:
            return {'message': 'Erro ao criar status.' + e}, 500

    # @jwt_required
    def get(self):
        parametro = request.get_json(force=True)
        id_pedido = parametro.get('id_pedido')
        return StatusModel.return_by_id_pedido(id_pedido)

    # @jwt_required
    def delete(self):
        parametro = request.get_json(force=True)
        id = parametro.get('id')
        try:
            StatusModel.delete_by_id(id)
            return {'message': 'Status deletado com sucesso.'}, 200
        except Exception as e:
            return {'message': 'Erro ao deletar status.' + e}, 500


class Solicitante(Resource):
    # @jwt_required
    def post(self):
        parametro = request.get_json(force=True)
        nomeSolicitante = parametro.get('solicitante')
        novo_solicitante = SolicitanteModel(solicitante=nomeSolicitante)
        try:
            novo_solicitante.save_to_db()
            return {
                'message': 'Solicitante criado com sucesso.'
            }
        except Exception as e:
            return {'message': 'Erro ao criar solicitante.' + e}, 500

    # @jwt_required
    def get(self):
        # parametro = request.get_json(force=True)
        # id = parametro.get('id')
        # return SolicitanteModel.return_by_id(id)
        return SolicitanteModel.return_all()

    # @jwt_required
    def delete(self):
        parametro = request.get_json(force=True)
        id = parametro.get('id')
        try:
            SolicitanteModel.delete_by_id(id)
            return {'message': 'Solicitante deletado com sucesso.'}, 200
        except Exception as e:
            return {'message': 'Erro ao deletar solicitante.' + e}, 500


class Solicitacao(Resource):
    # @jwt_required
    def post(self):
        parametro = request.get_json(force=True)
        nomeSolicitacao = parametro.get('solicitacao')
        nova_solicitacao = SolicitacaoModel(solicitacao=nomeSolicitacao)
        try:
            nova_solicitacao.save_to_db()
            return {
                'message': 'Solicitacao criado com sucesso.'
            }
        except Exception as e:
            return {'message': 'Erro ao criar solicitacao.' + e}, 500

    # @jwt_required
    def get(self):
        # parametro = request.get_json(force=True)
        # id = parametro.get('id')
        # return SolicitacaoModel.return_by_id(id)
        return SolicitacaoModel.return_all()

    # @jwt_required
    def delete(self):
        parametro = request.get_json(force=True)
        id = parametro.get('id')
        try:
            SolicitacaoModel.delete_by_id(id)
            return {'message': 'Solicitacao deletada com sucesso.'}, 200
        except Exception as e:
            return {'message': 'Erro ao deletar solicitacao.' + e}, 500


class SlackResponse(Resource):

    def post(self):
        parametro = request.get_json(force=True)
        asw = parametro.get('asw')
        print(asw)
        return {'message': 'asw: ' + asw}, 200

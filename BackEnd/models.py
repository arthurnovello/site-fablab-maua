from run import db

class PedidoModel(db.Model):
    __tablename__ = 'Pedidos'
    id = db.Column(db.Integer, primary_key=True)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('Pessoas.id'), nullable=False)
    id_solicitante = db.Column(db.Integer, db.ForeignKey('Solicitantes.id'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('Cursos.id'), nullable=False)
    id_solicitacao = db.Column(db.Integer, db.ForeignKey('Solicitacoes.id'), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('Salas.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.String, nullable=False)
    qtd_pessoas = db.Column(db.Integer, nullable=False)
    aprovado = db.Column(db.Boolean, nullable=False, default=False)
    prazo = db.Column(db.Boolean, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    material_proprio = db.Column(db.Boolean, nullable=False)

    @classmethod
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_by_email(cls, email):
        return cls.query('Pedidos').join('Pessoas').filter('Pedidos.id_pessoa' == 'Pessoas.id' and 'Pessoas.email' == email)

    @classmethod
    def delete_by_id(cls, id):
        cls.query.delete(cls)
        cls.commit()
    

class CursoModel(db.Model):
    __tablename__ = 'Cursos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    curso = db.Column(db.String(255), nullable=False)

    @classmethod
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_by_id(cls, id):
        def to_json(x):
            return {
                'id': x.id,
                'curso': x.curso
            }
        return {'Curso': list(map(lambda x: to_json(x),
                cls.query.filter_by(id=id)))}        

    @classmethod
    def delete_by_id(cls, id):
        cls.query.delete(cls)
        cls.commit()

class SolicitanteModel(db.Model):
    __tablename__ = 'Solicitantes'
    id = db.Column(db.Integer, primary_key=True)
    solicitante = db.Column(db.String(255), nullable=False)

    @classmethod
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_by_id(cls, id):
        def to_json(x):
            return {
                'id': x.id,
                'solicitante': x.solicitante

            }
        return {'Solicitante': list(map(lambda x: to_json(x),
                cls.query.filter_by(id=id)))}
        
    @classmethod
    def delete_by_id(cls, id):
        cls.query.delete(cls)
        cls.commit()

class SalaModel(db.Model):
    __tablename__ = 'Salas'
    id = db.Column(db.Integer, primary_key=True)
    sala = db.Column(db.String(255), nullable=False)

    @classmethod
    def save_to_db(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def return_by_id(cls, id):
        def to_json(x):
            return {
                'id': x.id,
                'sala': x.sala
            }
        return {'Sala': list(map(lambda x: to_json(x),
                cls.query.filter_by(id=id)))} 
       
    @classmethod
    def delete_by_id(cls, id):
        cls.query.delete(cls)
        cls.commit()

class SolicitacaoModel(db.Model):
    __tablename__ = 'Solicitacoes'
    id = db.Column(db.Integer, primary_key=True)
    solicitacao = db.Column(db.String(255), nullable=False)

    @classmethod
    def save_to_db(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def return_by_id(cls, id):
        def to_json(x):
            return {
                'id': x.id,
                'solicitacao': x.solicitacao

            }
        return {'Solicitacao': list(map(lambda x: to_json(x),
                cls.query.filter_by(id=id)))}
       
    @classmethod
    def delete_by_id(cls, id):
        cls.query.delete(cls)
        cls.commit()

class PessoaModel(db.Model):
    __tablename__ = 'Pessoas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    ra = db.Column(db.String(255), nullable=True)

    @classmethod
    def save_to_db(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def return_by_id(cls, id):
        def to_json(x):
            return {
                'id': x.id,
                'nome': x.nome,
                'email': x.email,
                'ra': x.ra

            }
        return {'Pessoa': list(map(lambda x: to_json(x),
                cls.query.filter_by(id=id)))}        
       
    @classmethod
    def delete_by_id(cls, id):
        cls.query.delete(cls)
        cls.commit()

class StatusModel(db.Model):
    __tablename__ = 'Status'
    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('Pedidos.id'), nullable=False)
    termino = db.Column(db.DateTime, nullable=False)
    massa = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.String(255), nullable=True)
    concluido = db.Column(db.Boolean, default=False)

    @classmethod
    def save_to_db(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def return_by_id(cls, id):
        def to_json(x):
            return {
                'id': x.id,
                'id_pedido': x.id_pedido,
                'termino': x.termino,
                'massa': x.massa,
                'tempo': x.tempo,
                'concluido': x.concluido
            }
        return {'Status': list(map(lambda x: to_json(x),
                cls.query.filter_by(id=id)))} 
       
    @classmethod
    def delete_by_id(cls, id):
        cls.query.delete(cls)
        cls.commit()
from CallSim import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    usuario = db.Column(db.String(length=100), nullable=False, unique=True)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    senha = db.Column(db.String(length=60), nullable=False, unique=True)
    lembrete_senha = db.Column(db.String(length=100), nullable=False, unique=True)

    @property
    def senhacript(self):
        return self.senhacrip

    @senhacript.setter
    def senhacript(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')

    def converte_senha(self, senha_texto_claro):
        return bcrypt.check_password_hash(self.senha, senha_texto_claro)

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitacao = db.Column(db.String(250), nullable=False)
    assunto = db.Column(db.String(220), nullable=False)
    id_os_corporate = db.Column(db.String(50), nullable=False)
    tipo_solicitacao = db.Column(db.String(220), nullable=False)
    produto = db.Column(db.String(220), nullable=False)
    contrato_item = db.Column(db.String(20), nullable=False)
    nome_cliente = db.Column(db.String(220), nullable=False)
    nome_contato = db.Column(db.String(220), nullable=False)
    telefone_contato = db.Column(db.String(220), nullable=False)
    email_contato = db.Column(db.String(220), nullable=False)
    descricao = db.Column(db.String(220), nullable=False)
    historico_mensagem = db.Column(db.String(250), nullable=False)
    situacao = db.Column(db.String(100), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(250), nullable=False)

class TipoDeSolicitacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitacao = db.Column(db.String(250), nullable=False)

class Situacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    situacao = db.Column(db.String(250), nullable=False)

class Assunto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assunto = db.Column(db.String(250), nullable=False)

class ChamadoEncerrado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitacao = db.Column(db.String(250), nullable=False)
    assunto = db.Column(db.String(220), nullable=False)
    id_os_corporate = db.Column(db.String(50), nullable=False)
    tipo_solicitacao = db.Column(db.String(220), nullable=False)
    produto = db.Column(db.String(220), nullable=False)
    contrato_item = db.Column(db.String(20), nullable=False)
    nome_cliente = db.Column(db.String(220), nullable=False)
    nome_contato = db.Column(db.String(220), nullable=False)
    telefone_contato = db.Column(db.String(220), nullable=False)
    email_contato = db.Column(db.String(220), nullable=False)
    descricao = db.Column(db.String(220), nullable=False)
    historico_mensagem = db.Column(db.String(250), nullable=False)
    descricao_encerramento = db.Column(db.String(220), nullable=False)
    situacao = db.Column(db.String(100), nullable=False)


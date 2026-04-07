from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length, equal_to
from wtforms_sqlalchemy.fields import QuerySelectField
from CallSim.models import TipoDeSolicitacao, Produto, Assunto, Situacao


class UsuarioForm(FlaskForm):
    nome = StringField(label='Nome:', validators=[DataRequired()])
    usuario = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='E-mail:', validators=[Email(), DataRequired()])
    senha1 = PasswordField(label='Senha:', validators=[Length(min=4), DataRequired()])
    senha2 = PasswordField(label='Confirmação de Senha:', validators=[equal_to('senha1'), DataRequired()])
    lembrete_senha = StringField(label='Lembrete de Senha:', validators=[DataRequired()])
    submit = SubmitField(label='Cadastrar')

class LoginForm(FlaskForm):
    usuario = StringField('Usuário:', validators=[DataRequired()])
    senha = PasswordField('Senha:', validators=[DataRequired()])
    submit = SubmitField('Logar')

class LembrarSenhaForm(FlaskForm):
    nome = StringField(label='Nome Completo:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='E-mail:', validators=[DataRequired()])
    submit = SubmitField('Lembrar')

class ExcluirUsuarioForm(FlaskForm):
    submit = SubmitField('Excluir')

class ProdutoForm(FlaskForm):
    produto = StringField('Nome do Produto:', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class ExcluirProdutoForm(FlaskForm):
    submit = SubmitField('Excluir')

class SolicitacaoForm(FlaskForm):
    solicitacao = StringField('Nome da Solicitação:', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class SituacaoForm(FlaskForm):
    situacao = StringField('Nome da Situacao:', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class AssuntoForm(FlaskForm):
    assunto = StringField('Nome do Assunto:', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class ExcluirAssuntoForm(FlaskForm):
    submit = SubmitField('Excluir')

class ExcluirSolicitacaoForm(FlaskForm):
    submit = SubmitField('Excluir')

def choice_tipo_solicitacao_query():
    return TipoDeSolicitacao.query

def choice_tipo_produto_query():
    return Produto.query

def choice_assunto_query():
    return Assunto.query

def choice_situacao_query():
    return Situacao.query

class ChamadoForm(FlaskForm):
    solicitacao = StringField(label='Solicitação:', validators=[DataRequired()])
    assunto = QuerySelectField(label='Assunto:', query_factory=choice_assunto_query,
                                    get_label=lambda ass: f"{ass.assunto}", allow_blank=True, blank_text="Selecione")
    id_os_corporate = StringField(label='Id Corporate:', validators=[DataRequired()])
    tipo_solicitacao = QuerySelectField(label="Tipo de Solicitação", query_factory=choice_tipo_solicitacao_query,
                                        get_label=lambda ts: f"{ts.solicitacao}",
                                        allow_blank=True, blank_text="Selecione")
    produto = QuerySelectField(label="Produto:", query_factory=choice_tipo_produto_query,
                                        get_label=lambda pd: f"{pd.produto}",
                                        allow_blank=True, blank_text="Selecione")
    contrato_item = StringField(label='Contrato/Item:', validators=[DataRequired()])
    nome_cliente = StringField(label='Nome do Cliente:', validators=[DataRequired()])
    nome_contato = StringField(label='Contato:', validators=[DataRequired()])
    telefone_contato = StringField(label='Telefone:', validators=[DataRequired()])
    email_contato = StringField(label='E-mail:', validators=[DataRequired()])
    descricao = TextAreaField(label='Descrição:', validators=[DataRequired()])
    #historico_mensagem = TextAreaField(label='Histórico:', validators=[DataRequired()])
    situacao = QuerySelectField(label="Situação:", query_factory=choice_situacao_query,
                                        get_label=lambda st: f"{st.situacao}",
                                        allow_blank=True, blank_text="Selecione")
    submit = SubmitField('Abrir Chamado')

class ChamadoAlteradoForm(FlaskForm):
    solicitacao = StringField(label='Solicitação:', validators=[DataRequired()])
    assunto = StringField(label='Assunto:', validators=[DataRequired()])
    id_os_corporate = StringField(label='Id Corporate:', validators=[DataRequired()])
    tipo_solicitacao = StringField(label='Solicitação:', validators=[DataRequired()])
    produto = StringField(label='Produto:', validators=[DataRequired()])
    contrato_item = StringField(label='Contrato/Item:', validators=[DataRequired()])
    nome_cliente = StringField(label='Nome do Cliente:', validators=[DataRequired()])
    nome_contato = StringField(label='Contato:', validators=[DataRequired()])
    telefone_contato = StringField(label='Telefone:', validators=[DataRequired()])
    email_contato = StringField(label='E-mail:', validators=[DataRequired()])
    descricao = TextAreaField(label='Descrição:', validators=[DataRequired()])
    historico_mensagem = TextAreaField(label='Histórico:', validators=[DataRequired()])
    situacao = QuerySelectField(label="Situação:", query_factory=choice_situacao_query,
                                        get_label=lambda st: f"{st.situacao}",
                                        allow_blank=True, blank_text="Selecione")
    submit = SubmitField('Abrir Chamado')

class EncerrarChamadoForm(FlaskForm):
    solicitacao = StringField(label='Solicitação:', validators=[DataRequired()])
    assunto = StringField(label='Assunto:', validators=[DataRequired()])
    id_os_corporate = StringField(label='Id Corporate:', validators=[DataRequired()])
    tipo_solicitacao = StringField(label='Tipo de Solicitação:', validators=[DataRequired()])
    produto = StringField(label='Produto:', validators=[DataRequired()])
    contrato_item = StringField(label='Contrato/Item:', validators=[DataRequired()])
    nome_cliente = StringField(label='Nome do Cliente:', validators=[DataRequired()])
    nome_contato = StringField(label='Contato:', validators=[DataRequired()])
    telefone_contato = StringField(label='Telefone:', validators=[DataRequired()])
    email_contato = StringField(label='E-mail:', validators=[DataRequired()])
    descricao = TextAreaField(label='Descrição:', validators=[DataRequired()])
    historico_mensagem = TextAreaField(label='Histórico:', validators=[DataRequired()])
    descricao_encerramento = TextAreaField(label='Descrição de Encerramento:', validators=[DataRequired()])
    situacao = StringField(label='Situação:')

class FinalizarChamadoForm(FlaskForm):
    submit = SubmitField('Encerrar Chamado')

class ContatoForm(FlaskForm):
    submit = SubmitField('Encerrar Chamado')
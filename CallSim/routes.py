import io
from sqlite3 import IntegrityError
from sys import exception
from flask_login import login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, send_file
from CallSim import app, db
from CallSim.form import LoginForm, UsuarioForm, ProdutoForm, SolicitacaoForm, ChamadoForm, LembrarSenhaForm, \
    SituacaoForm, EncerrarChamadoForm, AssuntoForm, ChamadoAlteradoForm
from CallSim.models import Usuario, Produto, TipoDeSolicitacao, Chamado, Situacao, ChamadoEncerrado, Assunto
import pandas as pd

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        usuario_logado = Usuario.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)
            flash(f'Sucesso! {usuario_logado.usuario} logado com sucesso', category='success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorreto. Tente novamente', category='danger')

    return render_template('index.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    flash("Logou efetuado com sucesso.", category="info")
    return redirect(url_for('index'))

@app.route('/lembrar_senha/', methods=['GET', 'POST'])
def lembrar_senha():
    form = LembrarSenhaForm()
    resultado = None
    abrir_modal = False

    if form.validate_on_submit():
        resultado = Usuario.query.filter_by(
            nome = form.nome.data,
            email = form.email.data
        ).all()

        abrir_modal = True

    return render_template('lembrar_senha.html', form=form, resultado=resultado, abrir_modal=abrir_modal)

@app.route('/home/')
@login_required
def home():

    return render_template('home.html')

@app.route('/lista_usuario')
@login_required
def lista_usuario():

    dados_usuario = Usuario.query.all()
    if not dados_usuario:
        flash('Lista de Usuários ainda não possui dados.', category='warning')

    return render_template('lista_usuario.html', dados_usuario=dados_usuario)

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
@login_required
def cadastro_usuario():
    form = UsuarioForm()

    try:
        if form.validate_on_submit():
            usuario_existente = Usuario.query.filter((Usuario.usuario == form.usuario.data) | (Usuario.email == form.email.data)).first()

            if usuario_existente:
                flash('Usuário ou e-mail já cadastrados! Tente Novamente.', category='danger')
                return redirect(url_for('cadastro_usuario'))

            usuario = Usuario(
                nome = form.nome.data,
                usuario = form.usuario.data,
                email = form.email.data,
                senhacript = form.senha1.data,
                lembrete_senha = form.lembrete_senha.data
            )
            db.session.add(usuario)
            db.session.commit()

            flash(f"Usuário {usuario.nome} cadastrado com sucesso!", category='success')
            return redirect(url_for('lista_usuario'))

    except IntegrityError as ie:
        db.session.rollback()
        flash(f'Erro inesperado: {ie}', category='danger')

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                # Isso vai pegar o erro do EqualTo e transformar em Flash
                flash(f"Erro no campo {getattr(form, field).label.text}: {error}", category='danger')

    return render_template('cadastro_usuario.html', form=form)

@app.route('/excluir_usuario/<int:usuario_id>', methods=['POST'])
@login_required
def excluir_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    try:
        db.session.delete(usuario)
        db.session.commit()
        flash(f'Usuário {usuario.nome} excluido(a) com sucesso!', category='success')
    except exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir usuário: {e}', category='danger')
    return redirect(url_for('lista_usuario'))

@app.route('/itens/')
@login_required
def itens():

    return render_template('itens.html')

@app.route('/produto/', methods=['GET', 'POST'])
@login_required
def produto():
    form = ProdutoForm()

    dados_produto = Produto.query.all()
    if not dados_produto:
        flash('Lista de Produtos ainda não possui dados.', category='warning')

    if form.validate_on_submit():
        produto = Produto(
            produto = form.produto.data
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso.', category='success')
        return redirect(url_for('produto'))

    return render_template('produto.html', form=form, dados_produto=dados_produto)

@app.route('/excluir_produto/<int:produto_id>', methods=['POST'])
@login_required
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    try:
        db.session.delete(produto)
        db.session.commit()
        flash(f'Produto {produto.produto} excluido(a) com sucesso!', category='success')
    except exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir Produto: {e}', category='danger')
    return redirect(url_for('produto'))

@app.route('/solicitacao/', methods=['GET', 'POST'])
@login_required
def solicitacao():
    form = SolicitacaoForm()

    dados_solicitacao = TipoDeSolicitacao.query.all()
    if not dados_solicitacao:
        flash('Lista de Solicitações ainda não possui dados.', category='warning')

    if form.validate_on_submit():
        tipo_solicitacao = TipoDeSolicitacao(
            solicitacao = form.solicitacao.data
        )
        db.session.add(tipo_solicitacao)
        db.session.commit()
        flash('Solicitação cadastrada com sucesso.', category='success')
        return redirect(url_for('solicitacao'))

    return render_template('solicitacao.html', form=form, dados_solicitacao=dados_solicitacao)

@app.route('/excluir_solicitacao/<int:solicitacao_id>', methods=['POST'])
@login_required
def excluir_solicitacao(solicitacao_id):
    solicitacao = TipoDeSolicitacao.query.get_or_404(solicitacao_id)

    try:
        db.session.delete(solicitacao)
        db.session.commit()
        flash(f'Solicitação {solicitacao.solicitacao} excluido(a) com sucesso!', category='success')
    except exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir Solicitacao: {e}', category='danger')
    return redirect(url_for('solicitacao'))

@app.route('/situacao/', methods=['GET', 'POST'])
@login_required
def situacao():
    form = SituacaoForm()

    dados_situacao = Situacao.query.all()
    if not dados_situacao:
        flash('Lista de Situaçãos ainda não possui dados.', category='warning')

    if form.validate_on_submit():
        situacao = Situacao(
            situacao = form.situacao.data
        )
        db.session.add(situacao)
        db.session.commit()
        flash('Situação cadastrada com sucesso.', category='success')
        return redirect(url_for('situacao'))

    return render_template('situacao.html', form=form, dados_situacao=dados_situacao)

@app.route('/excluir_situacao/<int:situacao_id>', methods=['POST'])
@login_required
def excluir_situacao(situacao_id):
    situacao = Situacao.query.get_or_404(situacao_id)

    try:
        db.session.delete(situacao)
        db.session.commit()
        flash(f'Situação {situacao.situacao} excluido(a) com sucesso!', category='success')
    except exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir situacao: {e}', category='danger')
    return redirect(url_for('situacao'))

@app.route('/lista_chamado/', methods=['GET', 'POST'])
@login_required
def lista_chamado():
    dados_chamado = Chamado.query.all()
    if not dados_chamado:
        flash('Lista de Chamados ainda não possui dados.', category='warning')

    return render_template('lista_chamado.html', dados_chamado=dados_chamado)

@app.route('/abrir_chamado/', methods=['GET', 'POST'])
@login_required
def abrir_chamado():
    form = ChamadoForm()

    if form.validate_on_submit():
        chamado = Chamado(
            solicitacao = form.solicitacao.data,
            assunto = form.assunto.data.assunto,
            id_os_corporate = form.id_os_corporate.data,
            tipo_solicitacao = form.tipo_solicitacao.data.solicitacao,
            produto = form.produto.data.produto,
            contrato_item = form.contrato_item.data,
            nome_cliente = form.nome_cliente.data,
            nome_contato = form.nome_contato.data,
            telefone_contato = form.telefone_contato.data,
            email_contato = form.email_contato.data,
            descricao = form.descricao.data,
            historico_mensagem = "Informe uma mensagem",
            situacao = form.situacao.data.situacao
        )
        db.session.add(chamado)
        db.session.commit()
        flash(f'Chamado {chamado.solicitacao} aberto com sucesso!', category='success')
        return redirect(url_for('lista_chamado'))
    print(form.errors)
    if form.errors != {}:
        for err in form.errors.values():
            print(err)
            flash(f"Erro ao cadastrar Chamado {err}", category="danger")

    return render_template('abrir_chamado.html', form=form)

@app.route('/encerrar_chamado/<int:chamado_id>', methods=['GET', 'POST'])
@login_required
def encerrar_chamado(chamado_id):
    chamado_original = Chamado.query.get_or_404(chamado_id)

    form = EncerrarChamadoForm(obj=chamado_original)

    if form.validate_on_submit():
        # 3. Criar a nova instância da tabela de ENCERRAMENTO
        novo_encerramento = ChamadoEncerrado(
            solicitacao = form.solicitacao.data,
            assunto = form.assunto.data,
            id_os_corporate = form.id_os_corporate.data,
            tipo_solicitacao = form.tipo_solicitacao.data,
            produto = form.produto.data,
            contrato_item = form.contrato_item.data,
            nome_cliente = form.nome_cliente.data,
            nome_contato = form.nome_contato.data,
            telefone_contato = form.telefone_contato.data,
            email_contato = form.email_contato.data,
            descricao = form.descricao.data,
            historico_mensagem = form.historico_mensagem.data,
            descricao_encerramento = form.descricao_encerramento.data,
            situacao = "Fechado"
        )
        db.session.add(novo_encerramento)
        db.session.delete(chamado_original)
        db.session.commit()
        flash("Chamado encerrado com sucesso!", "success")
        return redirect(url_for('lista_chamado_encerrado'))

    return render_template('encerrar_chamado.html', form=form)

@app.route('/excluir_chamado/<int:chamado_id>', methods=['POST'])
@login_required
def excluir_chamado(chamado_id):
    chamado = Chamado.query.get_or_404(chamado_id)

    try:
        db.session.delete(chamado)
        db.session.commit()
        flash(f'Chamado {chamado.solicitacao} excluido(a) com sucesso!', category='success')
    except exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir chamado: {e}', category='danger')
    return redirect(url_for('lista_chamado'))

@app.route('/gerar_relatorio_chamado/', methods=['GET', 'POST'])
@login_required
def gerar_relatorio_chamado():
    # 1. SQLAlchemy: Seleciona todos os registros sem filtro
    query = db.select(Chamado)

    # 2. Pandas: Lê a query diretamente para um DataFrame
    df = pd.read_sql(query, db.engine)

    # 3. Memória: Cria o arquivo Excel em buffer (sem salvar no disco)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatorio_Geral')

    output.seek(0)

    # 4. Flask: Envia o arquivo para o navegador
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='relatorio_de_chamados.xlsx'
    )

@app.route('/gerar_relatorio_chamado_encerrado/', methods=['GET', 'POST'])
@login_required
def gerar_relatorio_chamado_encerrado():
    # 1. SQLAlchemy: Seleciona todos os registros sem filtro
    query = db.select(ChamadoEncerrado)

    # 2. Pandas: Lê a query diretamente para um DataFrame
    df = pd.read_sql(query, db.engine)

    # 3. Memória: Cria o arquivo Excel em buffer (sem salvar no disco)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatorio_chamados_encerrados')

    output.seek(0)

    # 4. Flask: Envia o arquivo para o navegador
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='relatorio_chamados_finalizados.xlsx'
    )

@app.route('/assunto/', methods=['GET', 'POST'])
@login_required
def assunto():
    form = AssuntoForm()

    dados_assunto = Assunto.query.all()
    if not dados_assunto:
        flash('Lista de Assunto ainda não possui dados.', category='warning')

    if form.validate_on_submit():
        assunto = Assunto(
            assunto = form.assunto.data
        )
        db.session.add(assunto)
        db.session.commit()
        flash('Assunto cadastrado com sucesso.', category='success')
        return redirect(url_for('assunto'))

    return render_template('assunto.html', form=form, dados_assunto=dados_assunto)

@app.route('/excluir_assunto/<int:assunto_id>', methods=['POST'])
@login_required
def excluir_assunto(assunto_id):
    assunto = Assunto.query.get_or_404(assunto_id)

    try:
        db.session.delete(assunto)
        db.session.commit()
        flash(f'Assunto {assunto.assunto} excluido(a) com sucesso!', category='success')
    except exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir assunto: {e}', category='danger')
    return redirect(url_for('assunto'))

@app.route('/lista_chamado_encerrado/')
def lista_chamado_encerrado():
    dados_chamado_encerrado = ChamadoEncerrado.query.all()
    if not dados_chamado_encerrado:
        flash('Lista de Chamados ainda não possui dados.', category='warning')
    return render_template('lista_chamado_encerrado.html', dados_chamado_encerrado=dados_chamado_encerrado)

@app.route('/alterar_chamado/<int:chamado_id>', methods=['GET', 'POST'])
@login_required
def alterar_chamado(chamado_id):
    chamado = Chamado.query.get_or_404(chamado_id)

    form = ChamadoAlteradoForm(obj=chamado)

    if form.validate_on_submit():
        chamado.solicitacao = form.solicitacao.data
        chamado.assunto = form.assunto.data
        chamado.id_os_corporate = form.id_os_corporate.data
        chamado.tipo_solicitacao = form.tipo_solicitacao.data
        chamado.produto = form.produto.data
        chamado.contrato_item = form.contrato_item.data
        chamado.nome_cliente = form.nome_cliente.data
        chamado.nome_contato = form.nome_contato.data
        chamado.telefone_contato = form.telefone_contato.data
        chamado.email_contato = form.email_contato.data
        chamado.descricao = form.descricao.data
        chamado.historico_mensagem = form.historico_mensagem.data
        chamado.situacao = form.situacao.data.situacao

        db.session.commit()
        flash("Chamado Alterado com sucesso!", "success")
        return redirect(url_for('lista_chamado'))

    return render_template('alterar_chamado.html', form=form)




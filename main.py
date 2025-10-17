from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime, date
import fdb

app = Flask(__name__)

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\AURO.FDB'
user = 'sysdba'
password = 'sysdba'

app.secret_key = 'Auro2025'

con = fdb.connect(host=host, database=database, user=user, password=password)

@app.route('/')
def index():#def é um função
    usuario = session.get('usuario_logado')#pega o usuario logado
    tipo_usuario = session.get('tipo_usuario')#pega o tipo do usuario
    e_admin = (tipo_usuario == 1)#se o tipo do usuario for 1 é admin
    e_usuario = (tipo_usuario == 0)#se o tipo do usuario for 0 é usuario comum
    return render_template('index.html', usuario=usuario, e_admin=e_admin, e_usuario=e_usuario)

@app.route('/abrir_login')
def abrir_login():
    if session.get('usuario_logado'):#session.get se o usuario estiver logado
        if session.get('tipo_usuario') == 0:#usuario 0 e o admin 1
            return redirect(url_for('perfil_cliente'))
        return redirect(url_for('perfil_admin'))
    return render_template('login.html')

@app.route('/abrir_cadastro')
def abrir_cadastro():
    if session.get('usuario_logado'):
        flash('Deslogue antes de criar um novo cadastro.', 'erro')
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if session.get('usuario_logado'):#se o usuario estiver logado.
        flash('Deslogue antes de criar um novo cadastro.', 'erro')#deslogue antes de criar um novo cadastro
        return redirect(url_for('index'))

    etapa = request.form['etapa']

    if etapa == '1':
        nome = request.form['nome']#pega o nome do formulario
        cpf = request.form['cpf']#pega o cpf do formulario
        data_nasc_str = request.form['dataNascimento']
        nascimento = datetime.strptime(data_nasc_str, '%Y-%m-%d').date()
        hoje = date.today()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        if idade < 18:
            flash('Você precisa ter pelo menos 18 anos para se cadastrar.', 'erro')
            return redirect(url_for('abrir_cadastro'))
        cursor = con.cursor()
        try:
            cursor.execute("SELECT 1 FROM USUARIO WHERE CPF = ?", (cpf,))
            if cursor.fetchone():
                flash('CPF já cadastrado.', 'erro')
                return render_template('cadastro.html', etapa=1)
        finally:
            cursor.close()
        session['nome'] = nome
        session['cpf'] = cpf
        session['dataNascimento'] = data_nasc_str
        return render_template('cadastro.html', etapa=2)
    elif etapa == '2':
        email = request.form['email']
        cripyt_senha = request.form['senha']
        cursor = con.cursor()
        try:
            cursor.execute("SELECT 1 FROM USUARIO WHERE EMAIL = ?", (email,))
            if cursor.fetchone():
                flash('E-mail já cadastrado.', 'erro')
                return render_template('cadastro.html', etapa=2)
        finally:
            cursor.close()
        session['email'] = email
        session['senha'] = generate_password_hash(cripyt_senha).decode('utf-8')
        return render_template('cadastro.html', etapa=3)
    elif etapa == '3':
        confirmaEmail = request.form['confirmaEmail']
        confirmaCpf = request.form['confirmaCpf']
        confirmaNome = request.form['confirmaNome']
        confirmaDataNascimento = request.form['confirmaDataNascimento']
        nascimento = datetime.strptime(confirmaDataNascimento, '%Y-%m-%d').date()
        hoje = date.today()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        if idade < 18:
            flash('Você precisa ter pelo menos 18 anos para se cadastrar.', 'erro')
            return render_template('cadastro.html', etapa=3)
        cursor = con.cursor()
        try:
            if confirmaCpf != session['cpf']:
                cursor.execute("SELECT 1 FROM USUARIO WHERE CPF = ?", (confirmaCpf,))
                if cursor.fetchone():
                    flash('CPF já cadastrado.', 'erro')
                    return render_template('cadastro.html', etapa=3)
            if confirmaEmail != session['email']:
                cursor.execute("SELECT 1 FROM USUARIO WHERE EMAIL = ?", (confirmaEmail,))
                if cursor.fetchone():
                    flash('E-mail já cadastrado.', 'erro')
                    return render_template('cadastro.html', etapa=3)
        except:
            flash('Erro ao verificar dados.', 'erro')
            return redirect(url_for('abrir_cadastro'))
        finally:
            cursor.close()
        if confirmaNome != session['nome']:
            session['nome'] = confirmaNome
        if confirmaEmail != session['email']:
            session['email'] = confirmaEmail
        if confirmaCpf != session['cpf']:
            session['cpf'] = confirmaCpf
        if confirmaDataNascimento != session['dataNascimento']:
            session['dataNascimento'] = confirmaDataNascimento
        cursor = con.cursor()
        try:
            cursor.execute("""
                           INSERT INTO USUARIO (NOME, EMAIL, SENHA, CPF, SITUACAO, TIPO, TENTATIVA, DATA_NASCIMENTO)
                           VALUES (?, ?, ?, ?, 0, 0, 0, ?)
                           """, (
                               session['nome'],
                               session['email'],
                               session['senha'],
                               session['cpf'],
                               session['dataNascimento']
                           ))
            con.commit()
            flash("Cadastro realizado com sucesso!", 'sucesso')
            return redirect(url_for('abrir_login'))
        finally:
            cursor.close()

@app.route('/login', methods=['POST'])
def login():
    cpf = request.form['cpf']
    senha = request.form['senha']
    valido = False
    cursor = con.cursor()
    try:
        cursor.execute("SELECT NOME FROM USUARIO WHERE CPF = ?", (cpf,))
        temcpf = cursor.fetchone()
        if not temcpf:
            flash('CPF não encontrado.', 'erro')
            return redirect(url_for('abrir_login'))
        nome = temcpf[0]
        # cursor.execute("SELECT SITUACAO FROM USUARIO WHERE CPF = ?", (cpf,))
        # situacao = cursor.fetchone()[0]
        # cursor.execute("SELECT SENHA FROM USUARIO WHERE CPF = ?", (cpf,))
        # senha_hash = cursor.fetchone()[0]
        # cursor.execute("SELECT TIPO FROM USUARIO WHERE CPF = ?", (cpf,))
        # tipo = cursor.fetchone()[0]
        # cursor.execute("SELECT TENTATIVA FROM USUARIO WHERE CPF = ?", (cpf,))
        # tentativas = cursor.fetchone()[0]

        usuario = cursor.execute("SELECT SITUACAO, SENHA, TIPO, TENTATIVA FROM USUARIO WHERE CPF = ?", (cpf,))

        situacao, senha_hash, tipo, tentativas = usuario.fetchone()

        if situacao == 1:
            flash('Conta inativa. Entre em contato com o suporte.', 'erro')
            return redirect(url_for('abrir_login'))
        if tipo == 1:
            if senha == senha_hash:
                valido = True
        else:
            if check_password_hash(senha_hash, senha):
                valido = True
        if valido:
            cursor.execute("UPDATE USUARIO SET TENTATIVA = 0 WHERE CPF = ?", (cpf,))
            con.commit()
            session['usuario_logado'] = True
            session['nome_usuario'] = nome
            session['cpf_usuario'] = cpf
            session['tipo_usuario'] = tipo
            session['senha_usuario'] = senha
            flash('Login realizado com sucesso!', 'sucesso')
            if tipo == 1:
                return redirect(url_for('perfil_admin'))
            else:
                return redirect(url_for('perfil_cliente'))
        else:
            if tipo == 1:
                flash('Senha incorreta.', 'erro')
                return redirect(url_for('abrir_login'))
            novas = tentativas + 1
            if novas >= 3:
                cursor.execute("""
                    UPDATE USUARIO
                    SET TENTATIVA = ?, SITUACAO = 1
                    WHERE CPF = ?
                """, (novas, cpf))
                flash('Conta bloqueada após 3 tentativas. Entre em contato com o suporte.', 'erro')
            else:
                cursor.execute("UPDATE USUARIO SET TENTATIVA = ? WHERE CPF = ?", (novas, cpf))
                flash(f'Senha incorreta.', 'erro')
            con.commit()
            return redirect(url_for('abrir_login'))
    finally:
        cursor.close()

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'sucesso')
    return redirect(url_for('index'))

@app.route('/perfil_admin')
def perfil_admin():
    if not session.get('usuario_logado') or session.get('tipo_usuario') != 1:
        flash('Somente administradores podem acessar esta página.', 'erro')
        return redirect(url_for('index'))
    cursor = con.cursor()
    try:
        cursor.execute("SELECT NOME, CPF FROM USUARIO WHERE TIPO=0")
        usuarios = cursor.fetchall()  # [(nome, cpf), ...]
        cursor.execute("SELECT NOME, CPF FROM USUARIO WHERE TIPO=1")
        adms = cursor.fetchall()
    finally:
        cursor.close()
    return render_template('perfil_adm.html', usuarios=usuarios, adms=adms)

@app.route('/perfil_cliente')
def perfil_cliente():
    if not session.get('usuario_logado'):
        flash('Você precisa estar logado para acessar o perfil.', 'erro')
        return redirect(url_for('abrir_login'))

    tipo_usuario = session.get('tipo_usuario')
    if tipo_usuario == 1:  # se for admin
        return redirect(url_for('perfil_admin'))

    cpf = session['cpf_usuario']
    nome = session['nome_usuario']
    cursor = con.cursor()
    try:
        cursor.execute("SELECT DATA_NASCIMENTO FROM USUARIO WHERE CPF = ?", (cpf,))
        user = cursor.fetchone()
        data_nascimento = user[0]
        return render_template('perfil.html',nome_usuario=nome,data_nascimento=data_nascimento,cpf=cpf)
    finally:
        cursor.close()


@app.route('/editar_usuario/<cpf>', methods=['GET', 'POST'])
def editar_usuario(cpf):
    if not session.get('usuario_logado'):
        flash('Você precisa estar logado para editar o perfil.', 'erro')
        return redirect(url_for('abrir_login'))

    tipo_usuario = session.get('tipo_usuario')
    e_admin = (tipo_usuario == 1)

    if tipo_usuario != 1:
        cpf = session['cpf_usuario']

    cursor = con.cursor()
    try:
        if request.method == 'POST':
            nome_novo = request.form['nome']
            cpf_novo = request.form['cpf']
            senha_form = request.form.get('senha', '')
            email_novo = request.form['email']
            data_novo = request.form['data_nascimento']

            nasc = datetime.strptime(data_novo, '%Y-%m-%d').date()
            hoje = date.today()
            idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            if idade < 18:
                flash('É preciso ter mais de 18 anos.', 'erro')
                return redirect(url_for('editar_usuario', cpf=cpf))

            if cpf_novo != cpf:
                cursor.execute("SELECT 1 FROM USUARIO WHERE CPF = ?", (cpf_novo,))
                if cursor.fetchone():
                    flash('CPF já cadastrado.', 'erro')
                    return redirect(url_for('editar_usuario', cpf=cpf))

            cursor.execute("SELECT EMAIL FROM USUARIO WHERE CPF = ?", (cpf,))
            email_atual = cursor.fetchone()[0]
            if email_novo != email_atual:
                cursor.execute("SELECT 1 FROM USUARIO WHERE EMAIL = ?", (email_novo,))
                if cursor.fetchone():
                    flash('Email já cadastrado.', 'erro')
                    return redirect(url_for('editar_usuario', cpf=cpf))

            if senha_form.strip():
                if not e_admin:
                    nova_hash = generate_password_hash(senha_form).decode('utf-8')
                    session['senha_usuario'] = senha_form
                else:
                    cursor.execute("SELECT SENHA FROM USUARIO WHERE CPF = ?", (cpf,))
                    nova_hash = cursor.fetchone()[0]
            else:
                cursor.execute("SELECT SENHA FROM USUARIO WHERE CPF = ?", (cpf,))
                nova_hash = cursor.fetchone()[0]

            if e_admin:
                situacao_nova = int(request.form.get('situacao', 1))
                cursor.execute("SELECT SITUACAO, TENTATIVA FROM USUARIO WHERE CPF = ?", (cpf,))
                situacao_atual, tentativas_atual = cursor.fetchone()
                if situacao_atual == 1 and situacao_nova == 0:
                    tentativas_nova = 0
                else:
                    tentativas_nova = tentativas_atual
            else:
                cursor.execute("SELECT SITUACAO, TENTATIVA FROM USUARIO WHERE CPF = ?", (cpf,))
                situacao_nova, tentativas_nova = cursor.fetchone()

            cursor.execute("""
                           UPDATE USUARIO
                           SET NOME            = ?,
                               CPF             = ?,
                               SENHA           = ?,
                               EMAIL           = ?,
                               DATA_NASCIMENTO = ?,
                               SITUACAO        = ?,
                               TENTATIVA       = ?
                           WHERE CPF = ?
                           """, (nome_novo, cpf_novo, nova_hash, email_novo, data_novo, situacao_nova, tentativas_nova, cpf))
            con.commit()

            if tipo_usuario == 0:
                session['nome_usuario'] = nome_novo
                session['cpf_usuario'] = cpf_novo

            flash('Perfil atualizado com sucesso!', 'sucesso')
            if tipo_usuario == 1:
                return redirect(url_for('visualizar_usuario', cpf=cpf_novo))
            else:
                return redirect(url_for('perfil_cliente'))
        else:
            cursor.execute("""
                           SELECT NOME, CPF, SENHA, EMAIL, DATA_NASCIMENTO, SITUACAO
                           FROM USUARIO
                           WHERE CPF = ?
                           """, (cpf,))
            usuario = cursor.fetchone()
            if not usuario:
                flash('Usuário não encontrado.', 'erro')
                return redirect(url_for('index'))
            nome = usuario[0]
            cpf_form = usuario[1]
            senha_texto = session.get('senha_usuario', '') if tipo_usuario == 0 else ''
            # senha_texto = usuario[2]
            email = usuario[3]
            data_nascimento = usuario[4]
            situacao = usuario[5]
            return render_template('editar_usuario.html', nome=nome, cpf=cpf_form,
                                   senha=senha_texto, email=email, data_nascimento=data_nascimento,
                                   situacao=situacao, e_admin=e_admin)
    finally:
        cursor.close()
@app.route('/admin/usuario/<cpf>')
def visualizar_usuario(cpf):
    if not session.get('usuario_logado') or session.get('tipo_usuario') != 1:
        flash('Acesso restrito.', 'erro')
        return redirect(url_for('index'))
    cursor = con.cursor()
    try:
        cursor.execute("SELECT NOME, CPF, EMAIL, DATA_NASCIMENTO FROM USUARIO WHERE CPF = ?", (cpf,))
        usuario = cursor.fetchone()
        if not usuario:
            flash('Usuário não encontrado.', 'erro')
            return redirect(url_for('perfil_admin'))
    finally:
        cursor.close()
    return render_template('perfil.html',
                           nome_usuario=usuario[0],
                           cpf=usuario[1],
                           email=usuario[2],
                           data_nascimento=usuario[3])
@app.route('/visualizar_adm')
def visualizar_adm():
    if not session.get('usuario_logado') or session.get('tipo_usuario') != 1:
        flash('Acesso negado.', 'erro')
        return redirect(url_for('index'))
    return render_template('cadastrar_adm.html')

@app.route('/admin/cadastrar_adm', methods=['POST'])
def cadastrar_adm():
    if not session.get('usuario_logado') or session.get('tipo_usuario') != 1:
        flash('Acesso negado: somente administradores podem cadastrar outros administradores.', 'erro')
        return redirect(url_for('index'))
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha = request.form.get('senha')

    cursor = con.cursor()
    try:
        cursor.execute("SELECT 1 FROM USUARIO WHERE CPF = ?", (cpf,))
        if cursor.fetchone():
            flash('CPF já cadastrado.', 'erro')
            return redirect(url_for('visualizar_adm'))

        cursor.execute("SELECT 1 FROM USUARIO WHERE EMAIL = ?", (email,))
        if cursor.fetchone():
            flash('E-mail já cadastrado.', 'erro')
            return redirect(url_for('visualizar_adm'))

        cursor.execute("""
            INSERT INTO USUARIO (NOME, EMAIL, SENHA, CPF, SITUACAO, TIPO, TENTATIVA, DATA_NASCIMENTO)
            VALUES (?, ?, ?, ?, 0, 1, 0, ?)
        """, (
            nome,
            email,
            senha,
            cpf,
            '2000-01-01'
        ))
        con.commit()
        flash('Administrador cadastrado com sucesso!', 'sucesso')
        return redirect(url_for('perfil_admin'))
    finally:
        cursor.close()

@app.route('/dashboard')
def dashboard():
    if not session.get('usuario_logado'):
        flash('Acesso restrito.', 'erro')
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/dashboard/simulacao')
def dashboard_simulacao():
    if not session.get('usuario_logado'):
        flash('Acesso restrito.', 'erro')
        return redirect(url_for('index'))
    return render_template('dashboard_simulacao.html')

@app.route('/dashboard/historico')
def dashboard_historico():
    if not session.get('usuario_logado'):
        flash('Acesso restrito.', 'erro')
        return redirect(url_for('index'))
    return render_template('dashboard_historico.html')

@app.route('/dashboard/movimentacoes')
def dashboard_movimentacoes():
    if not session.get('usuario_logado'):
        flash('Acesso restrito.', 'erro')
        return redirect(url_for('index'))
    return render_template('dashboard_extrato.html')

if __name__ == '__main__':
    app.run(debug=True)
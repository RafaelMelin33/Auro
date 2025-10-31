from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime, date
from validate_docbr import CPF
import fdb
app = Flask(__name__)


host = 'localhost'
database = r'C:\Users\Aluno\Desktop\AURO2.FDB'
user = 'sysdba'
password = 'sysdba'

app.secret_key = 'Auro2025'

con = fdb.connect(host=host, database=database, user=user, password=password)

def validaCpf(usercpf):
    cpf = CPF()
    return cpf.validate(usercpf)

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

        if validaCpf(cpf) == False:
            flash('CPF inválido!', 'erro')
            return redirect(url_for('abrir_cadastro'))
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
        if validaCpf(confirmaCpf) == False:
            flash('CPF inválido!', 'erro')
            return redirect(url_for('abrir_cadastro'))
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
        resultado = cursor.fetchone()
        if not resultado:
            flash('CPF não encontrado.', 'erro')
            return redirect(url_for('abrir_login'))
        nome = resultado[0]

        cursor.execute("SELECT SITUACAO, SENHA, TIPO, TENTATIVA, ID_USUARIO FROM USUARIO WHERE CPF = ?", (cpf,))
        usuario = cursor.fetchone()
        if not usuario:
            flash('Usuário não encontrado.', 'erro')
            return redirect(url_for('abrir_login'))
        situacao, senha_hash, tipo, tentativas, id_usuario = usuario

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
            # Armazenar dados na sessão, incluindo id_usuario
            session['usuario_logado'] = True
            session['nome_usuario'] = nome
            session['cpf_usuario'] = cpf
            session['tipo_usuario'] = tipo
            session['senha_usuario'] = senha
            session['id_usuario'] = id_usuario
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
                flash('Senha incorreta.', 'erro')
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
        usuarios = cursor.fetchall()
        cursor.execute("SELECT NOME, CPF FROM USUARIO WHERE TIPO=1")
        adms = cursor.fetchall()

        # Buscar taxas ordenadas por data
        cursor.execute("""
                       SELECT ID_TAXA, DESCRICAO, VALOR, DATA_INICIO, DATA_FINAL
                       FROM TAXA
                       ORDER BY DATA_INICIO, ID_TAXA DESC
                       """)
        taxas = cursor.fetchall()
    finally:
        cursor.close()
    return render_template('perfil_adm.html', usuarios=usuarios, adms=adms, taxas=taxas)


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
    id_usuario = session.get('id_usuario')

    cursor = con.cursor()
    try:
        cursor.execute("SELECT DATA_NASCIMENTO FROM USUARIO WHERE CPF = ?", (cpf,))
        user = cursor.fetchone()
        data_nascimento = user[0]

        # Buscar total de receitas
        cursor.execute("""
                       SELECT CAST(SUM(VALOR) AS DOUBLE PRECISION)
                       FROM MOVIMENTACAO
                       WHERE ID_USUARIO = ?
                         AND CONDICAO = 1
                       """, (id_usuario,))
        total_receitas = cursor.fetchone()[0] or 0

        # Buscar total de despesas
        cursor.execute("""
                       SELECT CAST(SUM(VALOR) AS DOUBLE PRECISION)
                       FROM MOVIMENTACAO
                       WHERE ID_USUARIO = ?
                         AND CONDICAO = 0
                       """, (id_usuario,))
        total_despesas = cursor.fetchone()[0] or 0

        # Calcular saldo
        saldo = total_receitas - total_despesas

        return render_template('perfil.html',
                               nome_usuario=nome,
                               data_nascimento=data_nascimento,
                               cpf=cpf,
                               saldo=saldo)
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
            if validaCpf(cpf_novo) == False:
                flash('CPF inválido!', 'erro')
                return redirect(url_for('editar_usuario', cpf=cpf))
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
        flash('Faça login para acessar o dashboard.', 'erro')
        return redirect(url_for('abrir_login'))

    id_usuario = session.get('id_usuario')
    cursor = con.cursor()
    try:

        cursor.execute("""
                       SELECT CAST(SUM(VALOR) AS DOUBLE PRECISION)
                       FROM MOVIMENTACAO
                       WHERE ID_USUARIO = ?
                         AND CONDICAO = 1
                       """, (id_usuario,))
        total_receitas = cursor.fetchone()[0] or 0

        cursor.execute("""
                       SELECT CAST(SUM(VALOR) AS DOUBLE PRECISION)
                       FROM MOVIMENTACAO
                       WHERE ID_USUARIO = ?
                         AND CONDICAO = 0
                       """, (id_usuario,))
        total_despesas = cursor.fetchone()[0] or 0

        saldo = total_receitas - total_despesas

    finally:
        cursor.close()

    return render_template('dashboard.html',
                           total_receitas=total_receitas,
                           total_despesas=total_despesas,
                           saldo=saldo)
@app.route('/dashboard_simulacao', methods=['GET', 'POST'])
def dashboard_simulacao():
    if not session.get('usuario_logado'):
        flash('Faça login para acessar a simulação.', 'erro')
        return redirect(url_for('abrir_login'))

    id_usuario = session.get('id_usuario')
    etapa = None

    if request.method == 'POST':
        try:
            valor_emp = float(request.form.get('valor', 0))
            parcelas = int(request.form.get('parcelas', 0))
        except ValueError:
            flash('Valor ou parcelas inválidos.', 'erro')
            return render_template('dashboard_simulacao.html')

        data = request.form.get('data')

        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT FIRST 1 VALOR
                FROM TAXA
                WHERE DATA_FINAL IS NULL
                ORDER BY DATA_INICIO DESC
            """)
            taxa_tupla = cursor.fetchone()
            taxa_porcentagem = float(taxa_tupla[0]) if taxa_tupla and taxa_tupla[0] is not None else 0.0

            mes = datetime.now().month
            cursor.execute("""
                SELECT CAST(SUM(VALOR) AS DOUBLE PRECISION)
                FROM MOVIMENTACAO
                WHERE ID_USUARIO = ? AND CONDICAO = 1 AND EXTRACT(MONTH FROM DATA_ATUAL) = ?
            """, (id_usuario, mes))
            total_receitas = cursor.fetchone()[0] or 0

            cursor.execute("""
                SELECT CAST(SUM(VALOR) AS DOUBLE PRECISION)
                FROM MOVIMENTACAO
                WHERE ID_USUARIO = ? AND CONDICAO = 0 AND EXTRACT(MONTH FROM DATA_ATUAL) = ?
            """, (id_usuario, mes))
            total_despesas = cursor.fetchone()[0] or 0

        finally:
            cursor.close()

        taxa_dec = taxa_porcentagem / 100.0

        if parcelas <= 0:
            flash('Número de parcelas inválido.', 'erro')
            return render_template('dashboard_simulacao.html')

        if taxa_dec <= 0.0:
            flash('Taxa inválida')
        else:
            valor_mensal = (valor_emp * taxa_dec) / (1 - (1 + taxa_dec) ** (-parcelas))

        valor_total = valor_mensal * parcelas

        saldo = float(total_receitas) - float(total_despesas)
        if saldo > 0:
            comprometimento = (valor_mensal / saldo) * 100
        else:
            comprometimento = None

        etapa = 2


        if comprometimento is None:
            risco = ''
        else:
            try:
                c = float(comprometimento)
                if c >= 30:
                    risco = 'Alto'
                elif c >= 20:
                    risco = 'Médio'
                else:
                    risco = 'Baixo'
            except Exception:
                risco = ''

        return render_template('dashboard_simulacao.html',
                               etapa=etapa,
                               valor_mensal=valor_mensal,
                               valor_total=valor_total,
                               total_receitas=total_receitas,
                               total_despesas=total_despesas,
                               saldo=saldo,
                               comprometimento=comprometimento,
                               taxa=taxa_porcentagem,
                               parcelas=parcelas,
                               valor_emprestimo=valor_emp,
                               risco=risco)
                               

    # GET
    return render_template('dashboard_simulacao.html')

@app.route('/dashboard_historico')
def dashboard_historico():
    if not session.get('usuario_logado'):
        flash('Faça login para acessar o histórico.', 'erro')
        return redirect(url_for('abrir_login'))
    return render_template('dashboard_historico.html')

@app.route('/dashboard/movimentacoes')
def dashboard_extrato():
    if not session.get('usuario_logado'):
        flash('Faça login para acessar as movimentações.', 'erro')
        return redirect(url_for('abrir_login'))

    id_usuario = session.get('id_usuario')
    cursor = con.cursor()
    try:
        cursor.execute("""
            SELECT DESCRICAO, VALOR, DATA_ATUAL, ID_MOVIMENTACAO
            FROM MOVIMENTACAO
            WHERE ID_USUARIO = ? AND CONDICAO = 1
            ORDER BY DATA_ATUAL DESC
        """, (id_usuario,))
        receitas = cursor.fetchall()

        cursor.execute("""
            SELECT DESCRICAO, VALOR, DATA_ATUAL, ID_MOVIMENTACAO
            FROM MOVIMENTACAO

            WHERE ID_USUARIO = ? AND CONDICAO = 0
            ORDER BY DATA_ATUAL DESC
        """, (id_usuario,))
        despesas = cursor.fetchall()

        cursor.execute("""
            SELECT CAST(SUM(VALOR) AS DOUBLE PRECISION)
            FROM MOVIMENTACAO
            WHERE ID_USUARIO = ? AND CONDICAO = 1
        """, (id_usuario,))
        total_receitas = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT CAST(SUM(VALOR) AS DOUBLE PRECISION)
            FROM MOVIMENTACAO
            WHERE ID_USUARIO = ? AND CONDICAO = 0
        """, (id_usuario,))
        total_despesas = cursor.fetchone()[0] or 0


    finally:
        cursor.close()

    return render_template('dashboard_extrato.html',
                           receitas=receitas,
                           despesas=despesas,
                           total_receitas=total_receitas,
                           total_despesas=total_despesas)

@app.route('/movimentacoes/cadastrar_despesa', methods=['GET', 'POST'])
def cadastrar_despesa():
    if not session.get('usuario_logado'):
        flash('Faça login para cadastrar despesa.', 'erro')
        return redirect(url_for('abrir_login'))
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        tipo = int(request.form['tipo'])
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO MOVIMENTACAO (DESCRICAO, VALOR, CONDICAO, TIPO, ID_USUARIO)
                VALUES (?, ?, 0, ?, ?)""",
                (descricao, valor, tipo, session.get('id_usuario')))
            con.commit()
            flash('Despesa cadastrada com sucesso!', 'sucesso')
            return redirect(url_for('dashboard_extrato'))
        finally:
            cursor.close()
    return render_template('cadastrar_despesa.html')

@app.route('/movimentacoes/cadastrar_receita', methods=['GET', 'POST'])
def cadastrar_receita():
    if not session.get('usuario_logado'):
        flash('Faça login para cadastrar receita.', 'erro')
        return redirect(url_for('abrir_login'))
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        tipo = int(request.form['tipo'])  # 0 = fixo, 1 = variável
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO MOVIMENTACAO (DESCRICAO, VALOR, CONDICAO, TIPO, ID_USUARIO)
                VALUES (?, ?, 1, ?, ?)""",
                (descricao, valor, tipo, session.get('id_usuario')))
            con.commit()
            flash('Receita cadastrada com sucesso!', 'sucesso')
            return redirect(url_for('dashboard_extrato'))
        finally:
            cursor.close()
    return render_template('cadastrar_receita.html')


@app.route('/admin/adicionar_taxa')
def visualizar_adicionar_taxa():
    if not session.get('usuario_logado') or session.get('tipo_usuario') != 1:
        flash('Acesso negado.', 'erro')
        return redirect(url_for('index'))
    return render_template('adicionar_taxa.html')

@app.route('/admin/cadastrar_taxa', methods=['POST'])
def cadastrar_taxa():
    if not session.get('usuario_logado') or session.get('tipo_usuario') != 1:
        flash('Acesso negado: somente administradores podem cadastrar taxas.', 'erro')
        return redirect(url_for('index'))
 
    descricao = request.form.get('descricao')
    valor = request.form.get('valor')
 
    cursor = con.cursor()
    try:
        # Checa se já existe uma taxa cadastrada hoje
        cursor.execute("""
            SELECT 1 FROM TAXA WHERE DATA_INICIO = CURRENT_DATE
        """)
        existe_taxa_hoje = cursor.fetchone()
 
        if existe_taxa_hoje:
            flash('Já existe uma taxa cadastrada hoje. Só é permitido cadastrar uma taxa por dia.', 'erro')
            return redirect(url_for('visualizar_adicionar_taxa'))
 
        # Atualiza a anterior e cadastra uma nova
        cursor.execute("""
            UPDATE TAXA
            SET DATA_FINAL = CURRENT_DATE
            WHERE DATA_FINAL IS NULL
        """)
        cursor.execute("""
            INSERT INTO TAXA (DESCRICAO, VALOR, DATA_INICIO, DATA_FINAL)
            VALUES (?, ?, CURRENT_DATE, NULL)
        """, (descricao, valor))
 
        con.commit()
        flash('Taxa cadastrada com sucesso!', 'sucesso')
        return redirect(url_for('perfil_admin'))
    except:
        flash(f'Erro ao cadastrar taxa', 'erro')
        return redirect(url_for('visualizar_adicionar_taxa'))
    finally:
        cursor.close()

@app.route('/movimentacoes/editar_receita/<int:id_movimentacao>', methods=['GET', 'POST'])
def editar_receita(id_movimentacao):
    if not session.get('usuario_logado'):
        flash('Faça login para editar receita.', 'erro')
        return redirect(url_for('abrir_login'))

    id_usuario = session.get('id_usuario')
    cursor = con.cursor()

    try:
        cursor.execute("""
                       SELECT ID_MOVIMENTACAO, DESCRICAO, VALOR, TIPO, CONDICAO
                       FROM MOVIMENTACAO
                       WHERE ID_MOVIMENTACAO = ?
                         AND ID_USUARIO = ?
                         AND CONDICAO = 1
                       """, (id_movimentacao, id_usuario))

        movimentacao = cursor.fetchone()

        if not movimentacao:
            flash('Receita não encontrada ou você não tem permissão para editá-la.', 'erro')
            return redirect(url_for('dashboard_extrato'))

        if request.method == 'POST':
            descricao = request.form['descricao']
            valor = request.form['valor']
            tipo = int(request.form['tipo'])

            cursor.execute("""
                           UPDATE MOVIMENTACAO
                           SET DESCRICAO = ?,
                               VALOR     = ?,
                               TIPO      = ?
                           WHERE ID_MOVIMENTACAO = ?
                             AND ID_USUARIO = ?
                           """, (descricao, valor, tipo, id_movimentacao, id_usuario))

            con.commit()
            flash('Receita atualizada com sucesso!', 'sucesso')
            return redirect(url_for('dashboard_extrato'))

        return render_template('editar_receita.html',
                               id_movimentacao=movimentacao[0],
                               descricao=movimentacao[1],
                               valor=movimentacao[2],
                               tipo=movimentacao[3])
    finally:
        cursor.close()


@app.route('/movimentacoes/editar_despesa/<int:id_movimentacao>', methods=['GET', 'POST'])
def editar_despesa(id_movimentacao):
    if not session.get('usuario_logado'):
        flash('Faça login para editar despesa.', 'erro')
        return redirect(url_for('abrir_login'))

    id_usuario = session.get('id_usuario')
    cursor = con.cursor()

    try:
        cursor.execute("""
                       SELECT ID_MOVIMENTACAO, DESCRICAO, VALOR, TIPO, CONDICAO
                       FROM MOVIMENTACAO
                       WHERE ID_MOVIMENTACAO = ?
                         AND ID_USUARIO = ?
                         AND CONDICAO = 0
                       """, (id_movimentacao, id_usuario))

        movimentacao = cursor.fetchone()

        if not movimentacao:
            flash('Despesa não encontrada ou você não tem permissão para editá-la.', 'erro')
            return redirect(url_for('dashboard_extrato'))

        if request.method == 'POST':
            descricao = request.form['descricao']
            valor = request.form['valor']
            tipo = int(request.form['tipo'])

            cursor.execute("""
                           UPDATE MOVIMENTACAO
                           SET DESCRICAO = ?,
                               VALOR     = ?,
                               TIPO      = ?
                           WHERE ID_MOVIMENTACAO = ?
                             AND ID_USUARIO = ?
                           """, (descricao, valor, tipo, id_movimentacao, id_usuario))

            con.commit()
            flash('Despesa atualizada com sucesso!', 'sucesso')
            return redirect(url_for('dashboard_extrato'))

        return render_template('editar_despesa.html',
                               id_movimentacao=movimentacao[0],
                               descricao=movimentacao[1],
                               valor=movimentacao[2],
                               tipo=movimentacao[3])
    finally:
        cursor.close()
@app.route('/movimentacoes/deletar_receita/<int:id_movimentacao>', methods=['GET', 'POST'])
def deletar_receita(id_movimentacao):
    if not session.get('usuario_logado'):
        flash('Faça login para deletar receita.', 'erro')
        return redirect(url_for('abrir_login'))

    id_usuario = session.get('id_usuario')
    cursor = con.cursor()

    try:
        cursor.execute("""
                       SELECT ID_MOVIMENTACAO
                       FROM MOVIMENTACAO
                       WHERE ID_MOVIMENTACAO = ?
                         AND ID_USUARIO = ?
                         AND CONDICAO = 1
                       """, (id_movimentacao, id_usuario))

        movimentacao = cursor.fetchone()

        if not movimentacao:
            flash('Receita não encontrada ou você não tem permissão para deletá-la.', 'erro')
            return redirect(url_for('dashboard_extrato'))

        cursor.execute("""
                       DELETE FROM MOVIMENTACAO
                       WHERE ID_MOVIMENTACAO = ?
                         AND ID_USUARIO = ?
                       """, (id_movimentacao, id_usuario))
        con.commit()
        flash('Receita deletada com sucesso!', 'sucesso')
    finally:
        cursor.close()

    return redirect(url_for('dashboard_extrato'))


@app.route('/movimentacoes/deletar_despesa/<int:id_movimentacao>', methods=['GET', 'POST'])
def deletar_despesa(id_movimentacao):
    if not session.get('usuario_logado'):
        flash('Faça login para deletar despesa.', 'erro')
        return redirect(url_for('abrir_login'))

    id_usuario = session.get('id_usuario')
    cursor = con.cursor()

    try:
        # Verificar se a despesa pertence ao usuário e se é despesa (CONDICAO = 0)
        cursor.execute("""
                       SELECT ID_MOVIMENTACAO
                       FROM MOVIMENTACAO
                       WHERE ID_MOVIMENTACAO = ?
                         AND ID_USUARIO = ?
                         AND CONDICAO = 0
                       """, (id_movimentacao, id_usuario))

        movimentacao = cursor.fetchone()

        if not movimentacao:
            flash('Despesa não encontrada ou você não tem permissão para deletá-la.', 'erro')
            return redirect(url_for('dashboard_extrato'))

        cursor.execute("""
                       DELETE FROM MOVIMENTACAO
                       WHERE ID_MOVIMENTACAO = ?
                         AND ID_USUARIO = ?
                       """, (id_movimentacao, id_usuario))
        con.commit()
        flash('Despesa deletada com sucesso!', 'sucesso')
    finally:
        cursor.close()
    return redirect(url_for('dashboard_extrato'))


@app.route('/admin/editar_taxa/<int:id_taxa>', methods=['GET', 'POST'])
def editar_taxa(id_taxa):
    if not session.get('usuario_logado') or session.get('tipo_usuario') != 1:
        flash('Acesso negado: somente administradores podem editar taxas.', 'erro')
        return redirect(url_for('index'))

    cursor = con.cursor()

    try:
        cursor.execute("SELECT ID_TAXA, DESCRICAO, VALOR FROM TAXA WHERE ID_TAXA = ?", (id_taxa,))
        taxa = cursor.fetchone()

        if not taxa:
            flash('Taxa não encontrada.', 'erro')
            return redirect(url_for('perfil_admin'))

        if request.method == 'POST':
            descricao = request.form.get('descricao')
            valor = request.form.get('valor')

            # CORRIGIDO: ID -> ID_TAXA
            cursor.execute("""
                           UPDATE TAXA
                           SET DESCRICAO = ?,
                               VALOR     = ?
                           WHERE ID_TAXA = ?
                           """, (descricao, valor, id_taxa))
            con.commit()
            flash('Taxa editada com sucesso!', 'sucesso')
            return redirect(url_for('perfil_admin'))

        return render_template('editar_taxa.html', taxa=taxa)

    except:
        flash(f'Erro ao editar taxa ', 'erro')
        return redirect(url_for('perfil_admin'))
    finally:
        cursor.close()

@app.route('/admin/deletar_taxa/<int:id_taxa>', methods=['GET', 'POST'])
def deletar_taxa(id_taxa):
    if not session.get('usuario_logado') or session.get('tipo_usuario') != 1:
        flash('Acesso negado: somente administradores podem deletar taxas.', 'erro')
        return redirect(url_for('index'))

    

    cursor = con.cursor()
    try:
        cursor.execute("SELECT ID_TAXA, DESCRICAO, VALOR FROM TAXA WHERE ID_TAXA = ?", (id_taxa,))
        taxa = cursor.fetchone()

        if not taxa:
            flash('Taxa não encontrada.', 'erro')
            return redirect(url_for('perfil_admin'))

        cursor.execute("DELETE FROM TAXA WHERE ID_TAXA = ?", (id_taxa,))
        con.commit()
        flash('Taxa excluída com sucesso!', 'sucesso')
        return redirect(url_for('perfil_admin'))
    except:
        flash(f'Erro ao excluir taxa ', 'erro')
        return redirect(url_for('perfil_admin'))
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(debug=True)

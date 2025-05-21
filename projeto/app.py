from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-session'

# Tela de login
@app.route('/home')
def raiz():
    return render_template('index.html')

# Validação de login
@app.route('/login', methods=['POST'])
def login():
    cpf = request.form['cpf']
    senha = request.form['password']

    db = mysql.connector.connect(
        host='201.23.3.86',
        port=5000,
        user='usr_aluno',
        password='usr_aluno123',
        database='aula_fatec'
    )
    mycursor = db.cursor()
    query = f"SELECT id, nome, cpf, senha FROM andre_tbusuarios WHERE cpf = '{cpf}' AND senha = '{senha}'"
    mycursor.execute(query)

    resultado = mycursor.fetchall()

    if resultado:
        usuario = resultado[0]
        session['usuario_id'] = usuario[0]  # salva o ID na sessão
        nome_usuario = usuario[1]
        return render_template('cadastrado.html', nome=nome_usuario)
    else:
        return render_template('index.html', senhaErrada='Usuário ou senha inválidos!')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html',
                           titulo='Cadastro de Usuário',
                           titulo_formulario='Cadastro de Usuário',
                           action='/cadastrar_usuario',
                           nome='',
                           cpf='',
                           senha='',
                           botao_submit='Cadastrar',
                           readonly='')

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    nome = request.form['nome']
    cpf = request.form['cpf']
    senha = request.form['senha']

    db = mysql.connector.connect(
        host='201.23.3.86',
        port=5000,
        user='usr_aluno',
        password='usr_aluno123',
        database='aula_fatec'
    )
    mycursor = db.cursor()
    query = f"INSERT INTO andre_tbusuarios (nome, cpf, senha) VALUES ('{nome}', '{cpf}', '{senha}')"
    mycursor.execute(query)
    db.commit()

    return redirect('/home')

@app.route('/excluir_usuario', methods=['GET'])
def exibir_formulario_exclusao():
    return render_template('excluir_usuario.html')


@app.route('/excluir_usuario', methods=['POST'])
def excluir_usuario():
    user_id = request.form['user']  # Agora está ativado!

    db = mysql.connector.connect(
        host='201.23.3.86',
        port=5000,
        user='usr_aluno',
        password='usr_aluno123',
        database='aula_fatec'
    )
    mycursor = db.cursor()
    query = "DELETE FROM andre_tbusuarios WHERE id = %s"
    mycursor.execute(query, (user_id,))
    db.commit()

    session.clear()  # encerra a sessão do usuário, se estiver logado
    return redirect('/home')

@app.route('/alterar_dados')
def alterar_dados():
    if 'usuario_id' not in session:
        return redirect('/home')

    user_id = session['usuario_id']

    db = mysql.connector.connect(
        host='201.23.3.86',
        port=5000,
        user='usr_aluno',
        password='usr_aluno123',
        database='aula_fatec'
    )
    cursor = db.cursor()
    cursor.execute("SELECT nome, cpf, senha FROM andre_tbusuarios WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()

    return render_template('cadastrar.html',
                           titulo='Alterar Dados',
                           titulo_formulario='Alterar Seus Dados',
                           action='/salvar_alteracao',
                           nome=usuario[0],
                           cpf=usuario[1],
                           senha=usuario[2],
                           botao_submit='Salvar Alterações',
                           readonly='readonly')

@app.route('/salvar_alteracao', methods=['POST'])
def salvar_alteracao():
    if 'usuario_id' not in session:
        return redirect('/home')

    user_id = session['usuario_id']
    nome = request.form['nome']
    senha = request.form['senha']

    db = mysql.connector.connect(
        host='201.23.3.86',
        port=5000,
        user='usr_aluno',
        password='usr_aluno123',
        database='aula_fatec'
    )
    cursor = db.cursor()
    cursor.execute("UPDATE andre_tbusuarios SET nome = %s, senha = %s WHERE id = %s", (nome, senha, user_id))
    db.commit()

    return redirect('/home')

#app.run(debug=True)
app.run(debug=True)
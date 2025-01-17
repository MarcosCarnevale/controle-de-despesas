from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from passlib.hash import pbkdf2_sha256

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and pbkdf2_sha256.verify(senha, usuario[3]):
            session['user_id'] = usuario[0]
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.home'))
        else:
            flash('Email ou senha incorretos.', 'error')

    return render_template('login.html')

@auth_bp.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar-senha']

        # Validação tamanho de senha
        if len(senha) < 6:
            flash('A senha deve ter no mínimo 6 caracteres.', 'error')
            return redirect(url_for('auth.cadastrar_usuario'))

        # Validação de senha
        if senha != confirmar_senha:
            flash('As senhas não coincidem. Por favor, volte e corrija.', 'error')
            return redirect(url_for('auth.cadastrar_usuario'))

        conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            SELECT * FROM usuarios WHERE email = ?
        ''', (email,))
        usuario = cursor.fetchone()

        if usuario:
            conn.close()
            flash('O email já está cadastrado. Tente outro.', 'error')
            return redirect(url_for('auth.cadastrar_usuario'))

        senha = pbkdf2_sha256.hash(senha)

        try:
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha)
                VALUES (?, ?, ?)
            ''', (nome, email, senha))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash('O email já está cadastrado. Tente outro.', 'error')
            return redirect(url_for('auth.cadastrar_usuario'))

        conn.close()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('cadastrar_usuario.html')

@auth_bp.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('home.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('auth.login'))
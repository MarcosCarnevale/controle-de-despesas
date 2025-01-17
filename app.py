from flask import Flask
from routes.auth import auth_bp
from routes.banco import banco_bp
from routes.categoria import categoria_bp
from routes.pagamento import pagamento_bp
from routes.cartao import cartao_bp
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para usar mensagens flash

def create_tables():
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            numero TEXT NOT NULL,
            agencia TEXT NOT NULL,
            conta TEXT NOT NULL,
            dv TEXT NOT NULL,
            tipo_conta TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operacao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            subcategoria TEXT NOT NULL,
            descricao TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            numero TEXT NOT NULL,
            data_fechamento TEXT NOT NULL,
            data_vencimento TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.before_first_request
def initialize():
    create_tables()

app.register_blueprint(auth_bp)
app.register_blueprint(banco_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(pagamento_bp)
app.register_blueprint(cartao_bp)

if __name__ == '__main__':
    app.run(debug=True)
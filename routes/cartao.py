from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import sqlite3

cartao_bp = Blueprint('cartao', __name__)

@cartao_bp.route('/cadastrar_cartao', methods=['GET', 'POST'])
def cadastrar_cartao():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        numero = request.form['numero']
        data_fechamento = request.form['data_fechamento']
        data_vencimento = request.form['data_vencimento']

        conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cartoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                numero TEXT NOT NULL,
                data_fechamento INTEGER NOT NULL,
                data_vencimento INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO cartoes (nome, numero, data_fechamento, data_vencimento)
            VALUES (?, ?, ?, ?)
        ''', (nome, numero, data_fechamento, data_vencimento))
        conn.commit()
        conn.close()

        flash('Cartão cadastrado com sucesso!', 'success')
        return redirect(url_for('cartao.cadastrar_cartao'))

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM bancos')
    bancos = cursor.fetchall()
    cursor.execute('SELECT cartoes.id, cartoes.nome, cartoes.numero, cartoes.data_fechamento, cartoes.data_vencimento FROM cartoes')
    cartoes = cursor.fetchall()
    conn.close()

    return render_template('cadastrar_cartao.html', bancos=bancos, cartoes=cartoes)

@cartao_bp.route('/editar_cartao/<int:id>', methods=['GET', 'POST'])
def editar_cartao(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        numero = request.form['numero']
        data_fechamento = request.form['data_fechamento']
        data_vencimento = request.form['data_vencimento']

        cursor.execute('''
            UPDATE cartoes
            SET nome = ?, numero = ?, data_fechamento = ?, data_vencimento = ?
            WHERE id = ?
        ''', (nome, numero, data_fechamento, data_vencimento, id))
        conn.commit()
        conn.close()

        flash('Cartão atualizado com sucesso!', 'success')
        return redirect(url_for('cartao.cadastrar_cartao'))

    cursor.execute('SELECT id, nome, numero, data_fechamento, data_vencimento FROM cartoes WHERE id = ?', (id,))
    cartao = cursor.fetchone()
    conn.close()

    return render_template('editar_cartao.html', cartao=cartao)

@cartao_bp.route('/excluir_cartao/<int:id>', methods=['POST'])
def excluir_cartao(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cartoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Cartão excluído com sucesso!', 'success')
    return redirect(url_for('cartao.cadastrar_cartao'))
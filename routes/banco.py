from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

banco_bp = Blueprint('banco', __name__)

@banco_bp.route('/cadastrar_banco', methods=['GET', 'POST'])
def cadastrar_banco():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        nome_banco = request.form['nome_banco']
        numero_banco = request.form['numero_banco']
        agencia = request.form['agencia']
        conta = request.form['conta']
        dv = request.form['dv']
        tipo_conta = request.form['tipo_conta']
        
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

        try:
            cursor.execute('''
                INSERT INTO bancos (nome, numero, agencia, conta, dv, tipo_conta)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome_banco, numero_banco, agencia, conta, dv, tipo_conta))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash('O banco já está cadastrado. Tente outro.', 'error')
            return redirect(url_for('banco.cadastrar_banco'))

        conn.close()
        flash('Banco cadastrado com sucesso!', 'success')
        return redirect(url_for('banco.cadastrar_banco'))

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, numero, agencia, conta, dv, tipo_conta FROM bancos')
    bancos = cursor.fetchall()
    conn.close()

    return render_template('cadastrar_banco.html', bancos=bancos)

@banco_bp.route('/editar_banco/<int:id>', methods=['GET', 'POST'])
def editar_banco(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome_banco = request.form['nome_banco']
        numero_banco = request.form['numero_banco']
        agencia = request.form['agencia']
        conta = request.form['conta']
        dv = request.form['dv']
        tipo_conta = request.form['tipo_conta']

        cursor.execute('''
            UPDATE bancos
            SET nome = ?, numero = ?, agencia = ?, conta = ?, dv = ?, tipo_conta = ?
            WHERE id = ?
        ''', (nome_banco, numero_banco, agencia, conta, dv, tipo_conta, id))
        conn.commit()
        conn.close()
        flash('Banco atualizado com sucesso!', 'success')
        return redirect(url_for('banco.cadastrar_banco'))

    cursor.execute('SELECT nome, numero, agencia, conta, dv, tipo_conta FROM bancos WHERE id = ?', (id,))
    banco = cursor.fetchone()
    conn.close()

    return render_template('editar_banco.html', banco=banco, id=id)

@banco_bp.route('/excluir_banco/<int:id>', methods=['POST'])
def excluir_banco(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bancos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Banco excluído com sucesso!', 'success')
    return redirect(url_for('banco.cadastrar_banco'))
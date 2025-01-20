from flask import Blueprint, request, jsonify, redirect, url_for, session, flash, render_template
import sqlite3

atualizacao_bp = Blueprint('atualizacao', __name__)

@atualizacao_bp.route('/atualizar_status/<int:id>', methods=['POST'])
def atualizar_status(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    status = request.json['status']

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE pagamentos SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@atualizacao_bp.route('/editar_pagamento/<int:id>', methods=['GET', 'POST'])
def editar_pagamento(id):
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data = request.form['data']
        categoria = request.form['categoria']
        subcategoria = request.form['subcategoria']
        banco = request.form['banco']
        cartao = request.form['cartao']

        conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pagamentos
            SET descricao = ?, valor = ?, data = ?, categoria = ?, subcategoria = ?, banco = ?, cartao = ?
            WHERE id = ?
        ''', (descricao, valor, data, categoria, subcategoria, banco, cartao, id))
        conn.commit()
        conn.close()
        flash('Pagamento atualizado com sucesso!', 'success')
        return redirect(url_for('cadastro.cadastrar_pagamento'))

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pagamentos WHERE id = ?', (id,))
    pagamento = cursor.fetchone()
    cursor.execute('SELECT DISTINCT categoria FROM categorias WHERE operacao = "despesa"')
    categorias = cursor.fetchall()
    cursor.execute('SELECT id, nome FROM bancos')
    bancos = cursor.fetchall()
    cursor.execute('SELECT nome FROM cartoes')
    cartoes = cursor.fetchall()
    cursor.execute('SELECT categoria, subcategoria FROM categorias WHERE operacao = "despesa"')
    subcategorias = cursor.fetchall()
    conn.close()

    return render_template('editar_pagamento.html', pagamento=pagamento, categorias=categorias, bancos=bancos, cartoes=[cartao[0] for cartao in cartoes], subcategorias=subcategorias)
from flask import Blueprint, request, jsonify, redirect, url_for, session, flash, render_template, make_response
import sqlite3
import csv
from io import StringIO

atualizacao_bp = Blueprint('atualizacao', __name__)

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


@atualizacao_bp.route('/pagar_pagamentos', methods=['POST'])
def pagar_pagamentos():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    ids = request.json.get('ids', [])
    if not ids:
        return jsonify({'success': False, 'message': 'Nenhum pagamento selecionado'}), 400

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    
    try:
        # Validando se todos os pagamentos selecionados possuem um banco associado
        # criando uma string com os ids dos pagamentos separados por vírgula
        if len(ids) == 1:
            id_str = str(ids[0])
        else:
            id_str = ','.join(id for id in ids)

        # Consulta SQL para verificar se todos os pagamentos selecionados possuem um banco associado
        query = f"""
                       SELECT 
                        id 
                       FROM pagamentos 
                       WHERE 
                        id IN ({id_str}) 
                        AND banco = ''
                       """
        
        # Executando a consulta
        cursor.execute(query)
        
        # Recuperando os ids dos pagamentos que não possuem um banco associado
        invalid_ids = [str(row[0]) for row in cursor.fetchall()]
        
        # Se existirem pagamentos sem banco associado
        # if 1==1: #
        if invalid_ids != []:
        # if len(invalid_ids) > 0:
            # Se algum pagamento não possuir um banco associado, retornar erro
            # e informar quais pagamentos não possuem banco associado
            # O status HTTP 422 é utilizado para indicar que a requisição foi bem sucedida, mas o servidor não pode processar a entidade enviada
            return jsonify({'success': False, 'message': 'Os pagamentos selecionados não possuem um banco associado', 'invalid_ids': invalid_ids}), 422
        else:
            # Se todos os pagamentos possuirem um banco associado, atualizar o status dos pagamentos para "pago"
            cursor.executemany('UPDATE pagamentos SET status = "Pago" WHERE id = ?', [(id,) for id in ids])
            conn.commit()

            return jsonify({'success': True, 'query': query, 'invalid_ids': invalid_ids})


    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
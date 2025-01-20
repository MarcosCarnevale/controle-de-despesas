from flask import Blueprint, request, redirect, url_for, session, flash, jsonify
import sqlite3

exclusao_bp = Blueprint('exclusao', __name__)

@exclusao_bp.route('/excluir_pagamento/<int:id>', methods=['POST'])
def excluir_pagamento(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pagamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Pagamento excluído com sucesso!', 'success')
    return redirect(url_for('cadastro.cadastrar_pagamento'))

@exclusao_bp.route('/apagar_selecao', methods=['POST'])
def apagar_selecao():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    ids = request.json.get('ids', [])
    if not ids:
        return jsonify({'success': False, 'message': 'Nenhum pagamento selecionado'}), 400

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.executemany('DELETE FROM pagamentos WHERE id = ?', [(id,) for id in ids])
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@exclusao_bp.route('/apagar_selecao_anexo', methods=['POST'])
def apagar_selecao_anexo():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    ids = request.json.get('ids', [])
    if not ids:
        return jsonify({'success': False, 'message': 'Nenhum pagamento selecionado'}), 400

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    for id in ids:
        cursor.execute('SELECT id FROM anexos WHERE pagamento_id = ?', (id,))
        anexo = cursor.fetchone()
        if not anexo:
            return jsonify({'success': False, 'message': f'Pagamento {id} não tem anexo'}), 400
        cursor.execute('DELETE FROM anexos WHERE pagamento_id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})
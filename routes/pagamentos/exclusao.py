from flask import Blueprint, request, jsonify, session
import sqlite3

exclusao_bp = Blueprint('exclusao', __name__)

@exclusao_bp.route('/excluir_pagamentos', methods=['POST'])
def excluir_pagamentos():
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

@exclusao_bp.route('/excluir_anexos', methods=['POST'])
def excluir_anexos():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    ids = request.json.get('ids', [])
    if not ids:
        return jsonify({'success': False, 'message': 'Nenhum pagamento selecionado'}), 400

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.executemany('DELETE FROM anexos WHERE pagamento_id = ?', [(id,) for id in ids])
    conn.commit()
    conn.close()

    return jsonify({'success': True})
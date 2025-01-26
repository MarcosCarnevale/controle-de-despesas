from flask import Blueprint, request, jsonify, redirect, url_for, session, flash, send_file, make_response
import sqlite3
from datetime import datetime
import io

anexo_bp = Blueprint('anexo', __name__)

@anexo_bp.route('/salvar_anexo', methods=['POST'])
def salvar_anexo():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    pagamento_id = request.form['pagamento_id']
    arquivo = request.files['arquivo']
    data_upload = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tipo_arquivo = arquivo.content_type
    tamanho_arquivo = len(arquivo.read())
    arquivo.seek(0)  # Reset file pointer to the beginning
    arquivo_blob = arquivo.read()
    nome_arquivo = arquivo.filename

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anexos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pagamento_id INTEGER NOT NULL,
            data_upload TEXT NOT NULL,
            tipo_arquivo TEXT NOT NULL,
            tamanho_arquivo INTEGER NOT NULL,
            arquivo BLOB NOT NULL,
            nome_arquivo TEXT,
            FOREIGN KEY (pagamento_id) REFERENCES pagamentos (id)
        )
    ''')

    # Verificar se já existe um anexo para o pagamento_id
    cursor.execute('SELECT id FROM anexos WHERE pagamento_id = ?', (pagamento_id,))
    anexo_existente = cursor.fetchone()

    if anexo_existente:
        # Atualizar o anexo existente
        cursor.execute('''
            UPDATE anexos
            SET data_upload = ?, tipo_arquivo = ?, tamanho_arquivo = ?, arquivo = ?, nome_arquivo = ?
            WHERE pagamento_id = ?
        ''', (data_upload, tipo_arquivo, tamanho_arquivo, arquivo_blob, nome_arquivo, pagamento_id))
    else:
        # Inserir um novo anexo
        cursor.execute('''
            INSERT INTO anexos (pagamento_id, data_upload, tipo_arquivo, tamanho_arquivo, arquivo, nome_arquivo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (pagamento_id, data_upload, tipo_arquivo, tamanho_arquivo, arquivo_blob, nome_arquivo))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Anexo salvo com sucesso!'})

@anexo_bp.route('/download_anexo/<int:id>', methods=['GET'])
def download_anexo(id):
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT arquivo, tipo_arquivo, nome_arquivo FROM anexos WHERE pagamento_id = ?', (id,))
    anexo = cursor.fetchone()
    conn.close()

    if not anexo:
        return jsonify({'success': False, 'message': 'Anexo não encontrado'}), 404

    else:
        return send_file(
            path_or_file=io.BytesIO(anexo[0]),
            as_attachment=True,
            mimetype=anexo[1],
            download_name=anexo[2]
        )
    
@anexo_bp.route('/apagar_anexo/<int:id>', methods=['POST'])
def apagar_anexo(id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM anexos WHERE pagamento_id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Anexo apagado com sucesso!'})
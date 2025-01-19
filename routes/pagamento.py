from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify, send_file
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import io

pagamento_bp = Blueprint('pagamento', __name__)

@pagamento_bp.route('/cadastrar_pagamento', methods=['GET', 'POST'])
def cadastrar_pagamento():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data = request.form['data']
        categoria = request.form['categoria']
        subcategoria = request.form['subcategoria']
        banco = request.form['banco']
        parcela = request.form['parcela']
        quantidade_parcelas = int(request.form['quantidade_parcelas']) if parcela == 'sim' else 1
        cartao = request.form['cartao']
        status = 'Em Aberto'
        anexo = request.files['anexo'].read() if 'anexo' in request.files else None

        conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                categoria TEXT NOT NULL,
                subcategoria TEXT NOT NULL,
                banco TEXT NULL,
                parcela TEXT NULL,
                quantidade_parcelas INTEGER,
                cartao TEXT,
                status TEXT NOT NULL,
                anexo BLOB
            )
        ''')

        if parcela == 'sim' and cartao:
            cursor.execute('SELECT data_vencimento, data_fechamento FROM cartoes WHERE nome = ?', (cartao,))
            cartao_info = cursor.fetchone()
            vencimento = int(cartao_info[0])
            fechamento = int(cartao_info[1])

            data_pagamento = datetime.strptime(data, '%Y-%m-%d')
            valor_parcela = valor / quantidade_parcelas

            for i in range(quantidade_parcelas):
                if data_pagamento.day > fechamento:
                    data_pagamento = data_pagamento.replace(day=vencimento) + relativedelta(months=1)
                else:
                    data_pagamento = data_pagamento.replace(day=vencimento)

                cursor.execute('''
                    INSERT INTO pagamentos (descricao, valor, data, categoria, subcategoria, banco, parcela, quantidade_parcelas, cartao, status, anexo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (descricao, valor_parcela, data_pagamento.strftime('%Y-%m-%d'), categoria, subcategoria, banco, f'{i+1}/{quantidade_parcelas}', quantidade_parcelas, cartao, status, anexo))

                data_pagamento += timedelta(days=30)
        else:
            cursor.execute('''
                INSERT INTO pagamentos (descricao, valor, data, categoria, subcategoria, banco, parcela, quantidade_parcelas, cartao, status, anexo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (descricao, valor, data, categoria, subcategoria, banco, None, quantidade_parcelas, cartao, status, anexo))

        conn.commit()
        conn.close()
        flash('Pagamento cadastrado com sucesso!', 'success')
        return redirect(url_for('pagamento.cadastrar_pagamento'))

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT categoria FROM categorias WHERE operacao = "despesa"')
    categorias = cursor.fetchall()
    cursor.execute('SELECT id, nome FROM bancos')
    bancos = cursor.fetchall()
    cursor.execute('SELECT nome FROM cartoes')
    cartoes = cursor.fetchall()
    cursor.execute('''
        SELECT p.id, p.descricao, p.valor, p.data, p.categoria, p.subcategoria, p.banco, p.parcela, p.quantidade_parcelas, p.cartao, p.status, a.id IS NOT NULL AS has_anexo
        FROM pagamentos p
        LEFT JOIN anexos a ON p.id = a.pagamento_id
    ''')
    pagamentos = cursor.fetchall()
    conn.close()

    return render_template('cadastrar_pagamento.html', categorias=categorias, bancos=bancos, cartoes=[cartao[0] for cartao in cartoes], pagamentos=pagamentos)

@pagamento_bp.route('/subcategorias/<categoria>', methods=['GET'])
def subcategorias(categoria):
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT subcategoria FROM categorias WHERE categoria = ?', (categoria,))
    subcategorias = cursor.fetchall()
    conn.close()
    return jsonify({'subcategorias': [subcategoria[0] for subcategoria in subcategorias]})

@pagamento_bp.route('/excluir_pagamento/<int:id>', methods=['POST'])
def excluir_pagamento(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pagamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Pagamento excluído com sucesso!', 'success')
    return redirect(url_for('pagamento.cadastrar_pagamento'))

@pagamento_bp.route('/atualizar_status/<int:id>', methods=['POST'])
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

@pagamento_bp.route('/editar_pagamento/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('pagamento.cadastrar_pagamento'))

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

@pagamento_bp.route('/despesas_por_mes')
def despesas_por_mes():
    categoria = request.args.get('categoria', '')

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()

    if categoria:
        cursor.execute('''
            SELECT strftime('%Y-%m', data) as mes, SUM(valor) as valor
            FROM pagamentos
            WHERE categoria = ?
            GROUP BY mes
            ORDER BY mes
        ''', (categoria,))
    else:
        cursor.execute('''
            SELECT strftime('%Y-%m', data) as mes, SUM(valor) as valor
            FROM pagamentos
            GROUP BY mes
            ORDER BY mes
        ''')

    despesas = cursor.fetchall()
    conn.close()

    despesas_por_mes = [{'mes': mes, 'valor': valor} for mes, valor in despesas]
    return jsonify(despesas_por_mes)

@pagamento_bp.route('/home')
def home():
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT categoria FROM categorias WHERE operacao = "despesa"')
    categorias = cursor.fetchall()
    conn.close()
    return render_template('home.html', categorias=categorias)

@pagamento_bp.route('/salvar_anexo', methods=['POST'])
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
            SET data_upload = ?, tipo_arquivo = ?, tamanho_arquivo = ?, arquivo = ?
            WHERE pagamento_id = ?
        ''', (data_upload, tipo_arquivo, tamanho_arquivo, arquivo_blob, pagamento_id))
    else:
        # Inserir um novo anexo
        cursor.execute('''
            INSERT INTO anexos (pagamento_id, data_upload, tipo_arquivo, tamanho_arquivo, arquivo)
            VALUES (?, ?, ?, ?, ?)
        ''', (pagamento_id, data_upload, tipo_arquivo, tamanho_arquivo, arquivo_blob))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Anexo salvo com sucesso!'})

@pagamento_bp.route('/download_anexo/<int:id>')
def download_anexo(id):
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT arquivo, tipo_arquivo FROM anexos WHERE pagamento_id = ?', (id,))
    anexo = cursor.fetchone()
    conn.close()

    if anexo and anexo[0]:
        return send_file(
            io.BytesIO(anexo[0]),
            mimetype=anexo[1],
            as_attachment=True,
            attachment_filename=f'anexo_{id}.{anexo[1].split("/")[-1]}'  # Define o nome do arquivo com base no tipo de arquivo
        )
    else:
        flash('Anexo não encontrado.', 'danger')
        return redirect(url_for('pagamento.cadastrar_pagamento'))
    
@pagamento_bp.route('/apagar_anexo/<int:id>', methods=['POST'])
def apagar_anexo(id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado'}), 401

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM anexos WHERE pagamento_id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Anexo apagado com sucesso!', 'success')
    return redirect(url_for('pagamento.cadastrar_pagamento'))
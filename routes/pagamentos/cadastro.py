from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

cadastro_bp = Blueprint('pagamento', __name__)

@cadastro_bp.route('/cadastrar_pagamento', methods=['GET', 'POST'])
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

    filtros = {
        'categoria': request.args.get('categoria', ''),
        'subcategoria': request.args.get('subcategoria', ''),
        'banco': request.args.get('banco', ''),
        'cartao': request.args.get('cartao', ''),
        'data_inicio': request.args.get('data_inicio', ''),
        'data_fim': request.args.get('data_fim', '')
    }

    return render_template('cadastrar_pagamento.html', categorias=categorias, bancos=bancos, cartoes=[cartao[0] for cartao in cartoes], pagamentos=pagamentos, filtros=filtros)

@cadastro_bp.route('/subcategorias/<categoria>', methods=['GET'])
def subcategorias(categoria):
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT subcategoria FROM categorias WHERE categoria = ?', (categoria,))
    subcategorias = cursor.fetchall()
    conn.close()
    return jsonify({'subcategorias': [subcategoria[0] for subcategoria in subcategorias]})
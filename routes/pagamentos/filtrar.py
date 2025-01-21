from flask import Blueprint, request, render_template, session, redirect, url_for, flash, jsonify
import sqlite3

filtrar_bp = Blueprint('filtrar', __name__)

@filtrar_bp.route('/filtrar_pagamento', methods=['GET'])
def filtrar_pagamento():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    categoria = request.args.get('categoria', '')
    subcategoria = request.args.get('subcategoria', '')
    banco = request.args.get('banco', '')
    cartao = request.args.get('cartao', '')
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')

    query = '''
        SELECT p.id, p.descricao, p.valor, p.data, p.categoria, p.subcategoria, p.banco, p.parcela, p.quantidade_parcelas, p.cartao, p.status, a.id IS NOT NULL AS has_anexo
        FROM pagamentos p
        LEFT JOIN anexos a ON p.id = a.pagamento_id
        WHERE 1=1
    '''
    params = []

    if categoria:
        query += ' AND p.categoria = ?'
        params.append(categoria)
    if subcategoria:
        query += ' AND p.subcategoria = ?'
        params.append(subcategoria)
    if banco:
        query += ' AND p.banco = ?'
        params.append(banco)
    if cartao:
        query += ' AND p.cartao = ?'
        params.append(cartao)
    if data_inicio:
        query += ' AND p.data >= ?'
        params.append(data_inicio)
    if data_fim:
        query += ' AND p.data <= ?'
        params.append(data_fim)

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    pagamentos = cursor.fetchall()
    conn.close()

    filtros = {
        'categoria': categoria,
        'subcategoria': subcategoria,
        'banco': banco,
        'cartao': cartao,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }

    return render_template('cadastrar_pagamento.html', pagamentos=pagamentos, filtros=filtros, categorias=[], bancos=[], cartoes=[])
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

categoria_bp = Blueprint('categoria', __name__)

@categoria_bp.route('/cadastrar_categoria', methods=['GET', 'POST'])
def cadastrar_categoria():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        operacao = request.form['operacao']
        categoria = request.form['categoria']
        subcategoria = request.form['subcategoria']
        descricao = request.form['descricao']
        
        conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operacao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                subcategoria TEXT NOT NULL,
                descricao TEXT NOT NULL
            )
        ''')

        try:
            cursor.execute('''
                INSERT INTO categorias (operacao, categoria, subcategoria, descricao)
                VALUES (?, ?, ?, ?)
            ''', (operacao, categoria, subcategoria, descricao))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash('A categoria já está cadastrada. Tente outra.', 'error')
            return redirect(url_for('categoria.cadastrar_categoria'))

        conn.close()
        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('categoria.cadastrar_categoria'))

    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, operacao, categoria, subcategoria, descricao FROM categorias')
    categorias = cursor.fetchall()
    conn.close()

    return render_template('cadastrar_categoria.html', categorias=categorias)

@categoria_bp.route('/editar_categoria/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        operacao = request.form['operacao']
        categoria = request.form['categoria']
        subcategoria = request.form['subcategoria']
        descricao = request.form['descricao']

        cursor.execute('''
            UPDATE categorias
            SET operacao = ?, categoria = ?, subcategoria = ?, descricao = ?
            WHERE id = ?
        ''', (operacao, categoria, subcategoria, descricao, id))
        conn.commit()
        conn.close()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('categoria.cadastrar_categoria'))

    cursor.execute('SELECT operacao, categoria, subcategoria, descricao FROM categorias WHERE id = ?', (id,))
    categoria = cursor.fetchone()
    conn.close()

    return render_template('editar_categoria.html', categoria=categoria, id=id)

@categoria_bp.route('/excluir_categoria/<int:id>', methods=['POST'])
def excluir_categoria(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('./contas_a_pagar/cnt_a_pg.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categorias WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('categoria.cadastrar_categoria'))
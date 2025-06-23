from flask import Flask, request, g, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初回リクエスト時にテーブルを作成
@app.before_request
def create_table():
    try:
        conn = get_db_connection()
        # テーブルが存在するか確認
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
        if not cursor.fetchone():
            conn.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    contents TEXT NOT NULL
                )
            ''')
            conn.execute('''
                INSERT INTO notes (title, contents)
                VALUES ('1Sample Note', '1This is a sample note.'),
                ('2Sample Note', '2This is a sample note.'),
                ('3Sample Note', '3This is a sample note.')
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"データベースエラー: {e}")
    finally:
        conn.close()

# ホームメニュー
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# メモの追加画面
@app.route('/add-note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        contents = request.form['contents']
        conn = get_db_connection()
        conn.execute('INSERT INTO notes (title, contents) VALUES (?, ?)', (title, contents))
        conn.commit()
        conn.close()
        return redirect('/notes')
    return render_template('add_note.html')

# メモの一覧表示
@app.route('/notes')
def note_list():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return render_template('note_list.html', notes=notes)

# メモの削除機能
@app.route('/delete-note/<int:id>', methods=['POST'])
def delete_note(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/notes')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

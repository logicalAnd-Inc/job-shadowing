import sqlite3
import sys
from pprint import pprint

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初回起動時にテーブルを作成ダミーデータを挿入
def create_table_at_first():
    conn = get_db_connection()
    try:
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
                VALUES ('タイトル', '内容')
            ''')
            conn.commit()
        else:
            pass
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (create_table_at_first): {e}")
    finally:
        conn.close()

# すべてのノートの取得
def get_all_notes():
    conn = get_db_connection()
    try:
        notes = conn.execute('SELECT * FROM notes').fetchall()
        return notes
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (get_all_notes): {e}")
        return []
    finally:
        conn.close()

# 検索したのノートの取得
def get_search_notes(title, contents): # 引数のデフォルト値は、呼び出し側でNoneを渡すことを前提にすれば不要
    conn = get_db_connection()
    notes = []
    try:
        query = "SELECT * FROM notes WHERE 1=1" 
        params = []

        if title:
            # タイトルが指定されている場合
            query += " AND title LIKE ?"
            params.append(f"%{title}%")

        if contents:
            # 内容が指定されている場合
            query += " AND contents LIKE ?"
            params.append(f"%{contents}%")
        notes = conn.execute(query, params).fetchall()
        return notes
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (get_search_notes): {e}")
        return []
    finally:
        conn.close()

# 指定されたidのノートを取得
def get_note_by_id(note_id):
    conn = get_db_connection()
    try:
        note = conn.execute('SELECT id, title, contents FROM notes WHERE id = ?', (note_id,)).fetchone()
        return note
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (get_note_by_id): {e}")
        return None
    finally:
        conn.close()

# ノートをcreateする
def insert_note_db(title, contents):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO notes (title, contents) VALUES (?, ?)', (title, contents))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (insert_note_db): {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# ノートをupdateする
def update_note_db(note_id, title, contents):
    conn = get_db_connection()
    try:
        conn.execute('UPDATE notes SET title = ?, contents = ? WHERE id = ?', (title, contents, note_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (update_note_db): {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# ノートをdeleteする
def delete_note_db(note_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,)) # ここを修正: (id,) -> (note_id,)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (delete_note_db): {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
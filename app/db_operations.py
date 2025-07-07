import sqlite3
import os

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# データベース接続関数
def get_db_connection_ingredient():
    conn_ingredient = sqlite3.connect('ingredients.db')
    conn_ingredient.row_factory = sqlite3.Row
    return conn_ingredient

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
                    contents TEXT NOT NULL,
                    images TEXT NOT NULL DEFAULT 'default_image.png'
                )
            ''')
            conn.execute('''
                INSERT INTO notes (title, contents, images)
                VALUES ('タイトル', '内容', 'default_image.png')
            ''')
            conn.commit()
        else:
            pass
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (create_table_at_first): {e}")
    finally:
        conn.close()

def create_table_at_first_ingredient():
    conn_ingredient = get_db_connection_ingredient()
    
    try:
        cursor = conn_ingredient.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ingredients'")
        if not cursor.fetchone():
            # ingredientsテーブルの作成
            conn_ingredient.execute('''
                CREATE TABLE IF NOT EXISTS ingredients (
                    notes_id INTEGER NOT NULL,
                    ingredient_id INTEGER NOT NULL,
                    ingredient TEXT NOT NULL,
                amount TEXT NOT NULL
                )
            ''')
            conn_ingredient.commit()
        else:
            pass
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (create_table_at_first_ingredient): {e}")
    finally:
        conn_ingredient.close()

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

# 指定されたidのノートを取得
def get_note_by_id(note_id):
    conn = get_db_connection()
    try:
        note = conn.execute('SELECT id, title, contents, images FROM notes WHERE id = ?', (note_id,)).fetchone()
        return note
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (get_note_by_id): {e}")
        return None
    finally:
        conn.close()

# ノートをcreateする
def insert_note_db(title, contents, images):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO notes (title, contents, images) VALUES (?, ?, ?)', (title, contents, images))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (insert_note_db): {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# ノートをupdateする
def update_note_db(note_id, title, contents, images):
    conn = get_db_connection()
    try:
        conn.execute('UPDATE notes SET title = ?, contents = ?, images = ? WHERE id = ?', (title, contents, images, note_id))
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

# 画像ファイル名の変更
def image_rename_primary(title, filepath):
    conn = get_db_connection()
    try:
        id = conn.execute('SELECT id FROM notes WHERE title = ?', (title,)).fetchone()[0]
        new_filepath = f'{id}.png'
        conn.execute('UPDATE notes SET images = ? WHERE id = ?', (new_filepath, id))
        conn.commit()
        os.rename(os.path.join('./static/images', filepath), f'./static/images/{new_filepath}')
        return True
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (image_rename_primary): {e}")
        return False
    finally:
        conn.close()

def insert_ingredient_db(note_id, ingredient_id, ingredient, amount):
    conn = get_db_connection_ingredient()
    try:
        conn.execute('INSERT INTO ingredients (notes_id, ingredient_id, ingredient, amount) VALUES (?, ?, ?, ?)', (note_id, ingredient_id, ingredient, amount))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (insert_ingredient_db): {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_last_note():
    conn = get_db_connection()
    try:
        last_note = conn.execute('SELECT id FROM notes ORDER BY id DESC LIMIT 1').fetchone()
        return last_note[0] if last_note else None
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました (get_last_note): {e}")
        return None
    finally:
        conn.close()
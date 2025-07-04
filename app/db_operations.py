import sqlite3
import os

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
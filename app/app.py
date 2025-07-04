from flask import Flask, request, render_template, redirect, url_for
from db_operations import create_table_at_first, get_all_notes, get_note_by_id, insert_note_db, update_note_db, delete_note_db, image_rename_primary
import os

app = Flask(__name__)

# 初回リクエスト時にテーブルを作成
@app.before_request
def create_table():
    create_table_at_first()

# ホームメニュー
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# メモの追加画面
@app.route('/add-note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        # 追加処理
        # 画像ファイルの保存
        file = request.files['images']
        filepath = os.path.join('./static/images', file.filename)
        file.save(filepath)
        # データベースにメモを追加
        title = request.form['title']
        contents = request.form['contents'] 
        images = os.path.basename(filepath)
        insert_note_db(title, contents, images)
        # 画像ファイル名の変更

        image_rename_primary(title, images)

        return redirect(url_for('note_list'))
    
    return render_template('add_note.html')

# メモの更新
@app.route('/update-note/<int:id>', methods=['GET', 'POST'])
def update_note(id):
    note = get_note_by_id(id)

    # メモがあるか確認
    if note is None:
        return "メモが見つかりませんでした。", 404

    # 更新処理
    if request.method == 'POST':
        # 画像ファイルの保存
        file = request.files['images']
        if file != note['images']:
            os.remove(os.path.join('./static/images', note['images']))
            filepath = os.path.join('./static/images', file.filename)
            file.save(filepath)
            images = os.path.basename(filepath)
        else:
            images = note['images']
        title = request.form['title']
        contents = request.form['contents']
        update_note_db(id, title, contents, images)
        # 画像ファイル名の変更
        image_rename_primary(title, images)
        return redirect(url_for('note_list'))
    
    return render_template('update_note.html', note=note)

# メモの一覧表示
@app.route('/notes')
def note_list():
    # メモを全件取得
    notes = get_all_notes()
    return render_template('note_list.html', notes=notes)

# メモの削除機能
@app.route('/delete-note/<int:id>', methods=['POST'])
def delete_note(id):
    # 削除処理
    note = get_note_by_id(id)
    os.remove(os.path.join('./static/images', note['images']))
    delete_note_db(id)
    return redirect(url_for('note_list'))

# 404画面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# 500画面
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

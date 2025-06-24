from flask import Flask, request, render_template, redirect, url_for
from db_operations import create_table_at_first, get_all_notes, get_note_by_id, insert_note_db, update_note_db, delete_note_db, get_search_notes

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
        title = request.form['title']
        contents = request.form['contents']
        insert_note_db(title, contents)
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
        title = request.form['title']
        contents = request.form['contents']
        update_note_db(id, title, contents)
        return redirect(url_for('note_list'))
    
    return render_template('update_note.html', note=note)

# メモの一覧表示
@app.route('/notes')
def note_list():
    # メモを全件取得
    notes = get_all_notes()
    return render_template('note_list.html', notes=notes)

@app.route('/notes/search', methods=['GET', 'POST'])
def search_note_list():
    if request.method == 'POST':
        title = request.form.get('title')
        contents = request.form.get('contents')
        notes = get_search_notes(title, contents)
    else:
        title = request.args.get('title')
        contents = request.args.get('contents')
        notes = get_search_notes(title, contents)
    return render_template('note_list.html', notes=notes)

# メモの削除機能
@app.route('/delete-note/<int:id>', methods=['POST'])
def delete_note(id):
    # 削除処理
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

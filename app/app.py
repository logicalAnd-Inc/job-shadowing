from flask import Flask, request, render_template, redirect, url_for
from db_operations import (
    create_table_at_first,
    create_table_at_first_ingredient,
    get_all_notes,
    get_note_by_id,
    get_last_note,
    get_ingredient_by_note_id,
    insert_note_db,
    insert_ingredient_db,
    update_note_db,
    delete_note_db,
    delete_ingredient_db,
)
from helper import (
    generate_unique_filename
)
import os

app = Flask(__name__)

# 初回リクエスト時にテーブルを作成
@app.before_request
def create_table():
    create_table_at_first()
    create_table_at_first_ingredient()

# ホームメニュー
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# メモの追加画面
@app.route('/add-note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        # 画像ファイルの保存と判定
        last_note = get_last_note()
        file = request.files.get('images')
        if file and file.filename:
            images = generate_unique_filename(file.filename)
            filepath = os.path.join('./static/images', images)
            file.save(filepath)
        else:
            images = 'default_image.png'

        # データベースにメモを追加
        title = request.form['title']
        contents = request.form['contents']
        insert_note_db(title, contents, images)

        # 材料をデータベースに保存
        ingredients = []
        amounts = []
        ingredients = request.form.getlist('ingredient')
        amounts = request.form.getlist('amount')
        for i in range(len(ingredients)):
            insert_ingredient_db(last_note, i + 1, ingredients[i], amounts[i])
        return redirect(url_for('note_list'))
    
    return render_template('add_note.html')

# メモの更新
@app.route('/update-note/<int:id>', methods=['GET', 'POST'])
def update_note(id):
    note = get_note_by_id(id)
    ingredient = get_ingredient_by_note_id(id)

    # メモがあるか確認
    if note is None:
        return "メモが見つかりませんでした。", 404
    if ingredient is None:
        return "材料が見つかりませんでした。", 404

    # 更新処理
    if request.method == 'POST':
        # 画像ファイル名を取得
        file = request.files.get('images')
        # ファイルがなかった場合にはDBの画像名を使用
        if file is None or file.filename == '':
            images = note['images']
        else:
            if note['images'] != 'default_image.png':
                os.remove(os.path.join('./static/images', note['images']))
            images = generate_unique_filename(file.filename)
            filepath = os.path.join('./static/images', images)
            file.save(filepath)

        # メモの更新
        title = request.form['title']
        contents = request.form['contents']
        update_note_db(id, title, contents, images)

        # 材料の更新
        ingredients = []
        amounts = []
        last_note = get_last_note()
        ingredients = request.form.getlist('ingredient')
        amounts = request.form.getlist('amount')
        # 材料の削除
        delete_ingredient_db(id)
        # 材料の再登録
        for i in range(len(ingredients)):
            insert_ingredient_db(last_note, i + 1, ingredients[i], amounts[i])

        return redirect(url_for('note_list'))
    
    return render_template('update_note.html', note=note, ingredient=ingredient)

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
    if note['images'] != 'default_image.png':
        os.remove(os.path.join('./static/images', note['images']))
    delete_note_db(id)
    delete_ingredient_db(id)
    return redirect(url_for('note_list'))

# 404画面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# 500画面
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@app.route('/detail-note/<int:id>', methods=['GET'])
def detail_note(id):
    note = get_note_by_id(id)
    ingredient = get_ingredient_by_note_id(id)
    # メモがあるか確認
    if note is None:
        return "メモが見つかりませんでした。", 404
    else:
        return render_template('detail_note.html', note=note, ingredient=ingredient)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

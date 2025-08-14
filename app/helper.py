from datetime import datetime
import os

def generate_unique_filename(original_filename):
    """
    日付と時刻＋拡張子で一意なファイル名を生成する関数
    """
    ext = os.path.splitext(original_filename)[1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
    return f"{timestamp}{ext}"

def image_delete(image_name):
    """
    画像ファイルを削除する関数
    """
    if image_name and image_name != 'default_image.png':
        file_path = os.path.join('./static/images', image_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"画像ファイル {image_name} を削除しました。")
        else:
            print(f"画像ファイル {image_name} が見つかりません。")
    else:
        print("デフォルト画像は削除しません。")
    return None
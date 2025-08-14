from datetime import datetime
import os

def generate_unique_filename(original_filename):
    """
    日付と時刻＋拡張子で一意なファイル名を生成する関数
    """
    ext = os.path.splitext(original_filename)[1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
    return f"{timestamp}{ext}"
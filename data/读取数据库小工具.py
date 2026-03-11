import sqlite3
from pathlib import Path

file = input("文件：")
if not file:
    file = "spell_level"
file_name = file+".db"
BASE_DIR = Path(__file__).parent/file_name

conn = sqlite3.connect(BASE_DIR)
cursor = conn.cursor()
while True:
    q = input("你的诉求？或q退出:")
    if q == "q":
        conn.close()
        break
    else:
        try:
            cursor.execute(q)
            input(cursor.fetchall())
        except Exception as e:
            print(e)
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g, current_app
import math
from argon2 import PasswordHasher
from exceptions import *


def get_db():
    """获取数据库连接"""
    if "db" not in g:
        g.db = psycopg2.connect(
            current_app.config["DATABASE_URL"], cursor_factory=RealDictCursor
        )
    return g.db


def close_connection(exception=None):
    """关连接（注意这里去掉了 @app.teardown_appcontext，因为这里没有 app）"""
    db = g.pop("db", None)
    if db is not None:
        db.close()


# db只处理数据库问题，由api和search分别request关键词后调用
def get_info(kw, page, rpp, classMul, levelMul, schoolMul):
    conn = get_db()
    cursor = conn.cursor()
    offset = (page - 1) * rpp
    # 分开两个拼字符，算页码不得已而为之
    search_key = (
        "SELECT DISTINCT s.* FROM spells s JOIN levels l ON s.name = l.name WHERE 1=1 "
    )
    count_key = "SELECT COUNT(DISTINCT s.name) FROM spells s JOIN levels l ON s.name = l.name WHERE 1=1 "
    # 这里也用列表方便干净
    params = []
    if kw:
        search_key += (
            " AND (s.name ILIKE %s OR s.description ILIKE %s OR s.effect ILIKE %s)"
        )
        count_key += (
            " AND (s.name ILIKE %s OR s.description ILIKE %s OR s.effect ILIKE %s)"
        )
        params.extend([f"%{kw}%", f"%{kw}%", f"%{kw}%"])
    if classMul:
        search_key += " AND l.class = %s"
        count_key += " AND l.class = %s"
        params.extend([f"{classMul}"])
    if levelMul:
        levels_quest = ",".join("%s" for _ in levelMul)
        search_key += f" AND l.level IN ({levels_quest})"
        count_key += f" AND l.level IN ({levels_quest})"
        params.extend(levelMul)
    if not schoolMul:
        schoolMul = [
            "防护",
            "咒法",
            "预言",
            "惑控",
            "幻术",
            "死灵",
            "变化",
            "塑能",
            "通用",
        ]
    placeholder = ",".join("%s" for _ in schoolMul)
    search_key += f" AND s.school IN ({placeholder})"
    count_key += f" AND s.school IN ({placeholder})"
    params.extend(schoolMul)
    # 收集完毕，开始找总页码
    cursor.execute(count_key, tuple(params))
    total = cursor.fetchone()["count"]
    ttp = math.ceil(total / rpp)
    search_key += " ORDER BY s.name LIMIT %s OFFSET %s"
    params.extend([rpp, offset])
    params_tuple = tuple(params)
    # 找结果
    cursor.execute(search_key, params_tuple)
    row = cursor.fetchall()
    return {"row": row, "ttp": ttp, "total": total}


# 添加返回值total，预览总数


def get_details(spell_name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spells WHERE name ILIKE %s ", (spell_name,))
    rows = cursor.fetchone()
    cursor.execute("SELECT class,level FROM levels WHERE name ILIKE %s ", (spell_name,))
    rowl = cursor.fetchall()
    return (rows, rowl)


def init_db():
    """只是建表"""
    conn = get_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS spells (
            id          SERIAL PRIMARY KEY,
            name        TEXT NOT NULL UNIQUE,
            level_str   TEXT,
            school      TEXT,
            casting_time   TEXT,
            components  TEXT,
            range_      TEXT,
            effect      TEXT,
            aiming      TEXT,
            duration    TEXT,
            saving_throw TEXT,
            resistance  TEXT,
            description TEXT
        )
    """
        )
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS levels(
                   id    SERIAL PRIMARY KEY,
                   name  TEXT NOT NULL,
                   class Text,
                   level  TEXT)"""
        )
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS users(
                id            SERIAL PRIMARY KEY,
                username      TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                create_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        )
        cursor.execute(
            """
CREATE TABLE IF NOT EXISTS favorites(
                       user_id    INTEGER NOT NULL,
                       spell_name TEXT NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users(id),
                       FOREIGN KEY (spell_name) REFERENCES spells(name),
                       UNIQUE(user_id, spell_name))"""
        )


def register_user(username, password):
    conn = get_db()
    ph = PasswordHasher()
    with conn:
        cursor = conn.cursor()
        # 不要静默，重复创建或创建失败需要提示
        # 重复检验
        cursor.execute("SELECT * FROM users WHERE username=%s", (username.strip(),))
        i = cursor.fetchall()
        if i:
            raise NameCoincidence()
        insert_sql = """INSERT INTO users (username,password_hash) VALUES (%s,%s)"""
        password_hash = ph.hash(password)
        try:
            cursor.execute(
                insert_sql,
                (
                    username,
                    password_hash,
                ),
            )
            return True
        except Exception:
            return False


def verify_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    ph = PasswordHasher()
    cursor.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
    verify_pw = cursor.fetchone()  # 返回sqlite3.Row对象
    if verify_pw:
        try:
            # 从Row对象（字典）中取出字符串
            ph.verify(verify_pw["password_hash"], password)
            return True
        except Exception:
            return False


# 免得之后添加路由又要用add_favorite 之类的容易搞混，这里用favo代favorite得了
def add_favo(user_id, spell_name):
    conn = get_db()
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO favorites (user_id,spell_name) VALUES (%s,%s)",
                (
                    user_id,
                    spell_name,
                ),
            )
            # get_db 返回的是g对象，不用关闭
            return True
        except Exception as e:
            return e


def del_favo(user_id, spell_name):
    conn = get_db()
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM favorites WHERE user_id=%s AND spell_name=%s",
                (
                    user_id,
                    spell_name,
                ),
            )
            return True
        except Exception as e:
            return e


def get_favo_list(user_id):
    conn = get_db()
    try:  # SELECT 是查找，不需要with conn
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM favorites f JOIN spells s ON f.spell_name=s.name WHERE f.user_id=%s",
            (user_id,),
        )
        row = cursor.fetchall()
        results = row  # postgre返回的是字典列表
        return results
    except Exception as e:
        return e


def from_name_to_id(user_name):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s", (user_name,))
        row = cursor.fetchone()
        return row["id"]
    except Exception as e:
        return e

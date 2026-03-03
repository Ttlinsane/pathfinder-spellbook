import sqlite3
from flask import g, current_app
import math

def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_connection(exception=None):
    """关连接（注意这里去掉了 @app.teardown_appcontext，因为这里没有 app）"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

#db只处理数据库问题，由api和search分别request关键词后调用
def get_info(kw,page,rpp,classMul,levelMul,schoolMul):
    conn = get_db()
    cursor = conn.cursor()
    offset = (page-1)*rpp
    #分开两个拼字符，算页码不得已而为之
    search_key = "SELECT DISTINCT s.* FROM spells s JOIN levels l ON s.name = l.name WHERE 1=1 "
    count_key ="SELECT COUNT(DISTINCT s.name) FROM spells s JOIN levels l ON s.name = l.name WHERE 1=1 "
    #这里也用列表方便干净
    params = []
    if kw:
        search_key += " AND (s.name LIKE ? OR s.description LIKE ? OR s.effect LIKE ?)"
        count_key += " AND (s.name LIKE ? OR s.description LIKE ? OR s.effect LIKE ?)"
        params.extend([f"%{kw}%",f"%{kw}%",f"%{kw}%"])
    if classMul:   
        search_key += " AND l.class = ?"
        count_key += " AND l.class = ?"
        params.extend([f"{classMul}"])
    if levelMul:
        levels_quest = ",".join("?" for _ in levelMul)
        search_key += f" AND l.level IN ({levels_quest})"
        count_key += f" AND l.level IN ({levels_quest})"
        params.extend(levelMul)
    if not schoolMul:
        schoolMul=["防护","咒法","预言","惑控","幻术","死灵","变化","塑能","通用"]
    placeholder = ",".join("?" for _ in schoolMul)
    search_key += f" AND s.school IN ({placeholder})"
    count_key += f" AND s.school IN ({placeholder})"
    params.extend(schoolMul)
    #收集完毕，开始找总页码
    cursor.execute(count_key,tuple(params))
    total = cursor.fetchone()[0]
    ttp = math.ceil(total/rpp)
    search_key += " LIMIT ? OFFSET ?"
    params.extend([rpp,offset])
    params_tuple = tuple(params)
    #找结果
    cursor.execute(search_key,params_tuple)
    row = cursor.fetchall()
    return {"row":row,"ttp":ttp,"total":total}
#添加返回值total，预览总数

def get_details(spell_name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spells WHERE name=? COLLATE NOCASE", (spell_name,))
    rows = cursor.fetchone()
    cursor.execute("SELECT class,level FROM levels WHERE name=? COLLATE NOCASE",(spell_name,))
    rowl = cursor.fetchall()
    return (rows,rowl)
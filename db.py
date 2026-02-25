import sqlite3
from flask import g, current_app


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
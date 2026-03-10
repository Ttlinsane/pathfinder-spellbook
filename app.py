from flask import Flask, render_template
from db import close_connection,init_db
from config import Config
from routes.search import search_bp
from routes.api import api_bp
from routes.auth import auth_bp
from routes.favorites import favo_bp

app = Flask(__name__)
#注册config用作current.config
app.config.from_object(Config)

#原本该在设置里的，新版本Flask放在设置外了
#自动排序
app.json.sort_keys = False
#非英文转义
app.json.ensure_ascii = False
@app.route("/")
def index():
    return render_template("base-open.html")
app.teardown_appcontext(close_connection)
app.register_blueprint(search_bp)
app.register_blueprint(api_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(favo_bp)
#添加user表，但依赖g对象所以需要在上下文中

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
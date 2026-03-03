from routes.search import search_bp
from flask import Flask, render_template
from db import close_connection
from routes.api import api_bp
from config import Config

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
    return render_template("自我介绍.html")
app.teardown_appcontext(close_connection)
app.register_blueprint(search_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True)
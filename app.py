from flask import Flask, render_template,jsonify
from db import close_connection,init_db
from config import Config,DevConfig,ProdConfig
from routes.search import search_bp
from routes.api import api_bp
from routes.auth import auth_bp
from routes.favorites import favo_bp
from exceptions import *

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

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

    @app.errorhandler(UserError)
    def handle_user_error(e):
        return jsonify(e.to_dict()), e.http_status

    #添加user表，但依赖g对象所以需要在上下文中
    with app.app_context():
        init_db()
    return app

if __name__ == "__main__":
    app = create_app(DevConfig)
    app.run()

app = create_app(ProdConfig)
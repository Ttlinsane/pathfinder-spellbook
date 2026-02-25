from routes.search import search_bp
from flask import Flask, render_template
from db import close_connection
from config import Config

app = Flask(__name__)
#注册config用作current.config
app.config.from_object(Config)
@app.route("/")
def index():
    return render_template("自我介绍.html")
app.teardown_appcontext(close_connection)
app.register_blueprint(search_bp)

if __name__ == "__main__":
    app.run(debug=True)
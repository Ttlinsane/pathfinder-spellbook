from flask import Blueprint,session,request,url_for,redirect,render_template
from db import add_favo,del_favo,get_favo_list,from_name_to_id
from .helpers import login_required

favo_bp = Blueprint("favo",__name__,url_prefix="/user")

@favo_bp.route("/add",methods=["POST"])
@login_required  #先检测login状态才有session让你读
def add_favorite():
    if request.method == "POST":
        spell_name = request.form.get("spell_name")  #要在前端用POST方法get到，然后直接执行
        user_id = from_name_to_id(session["user"])
        result = add_favo(user_id,spell_name)  #因为在db里就做了try-except处理，所以这里似乎可以省略？
        if result:
            return redirect(url_for("search.search"))
        else:
            return result
@favo_bp.route("/del",methods=["POST"])
@login_required
def del_favorite():
    if request.method == "POST":
        spell_name = request.form.get("spell_name")
        user_id = from_name_to_id(session["user"])
        del_favo(user_id,spell_name)
        return redirect(url_for("search.search"))  #url_for("端点名而不是路径")，例如 ("search.search")应该是search文件的search端点

@favo_bp.route("/get",methods=["GET","POST"])
@login_required
def get_favorites():
    if request.method == "GET":
        user_id = from_name_to_id(session["user"])
        results = get_favo_list(user_id)
        return render_template("user.html", results = results)  #所以def index 的时候应该顺便运行一下这个？
#打算把这个结果直接列出在登录状态的主页上，在前端模板用{{for r in result}}...这样列出
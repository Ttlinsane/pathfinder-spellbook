from flask import Blueprint,request,session,redirect,render_template,url_for,jsonify
from db import verify_user,register_user
from .helpers import login_required
from exceptions import *

#注意格式！("...",__name__,prefix="...")
auth_bp = Blueprint("auth",__name__,url_prefix="/auth")

@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if verify_user(username,password):
            session['user']=username
            return redirect(url_for('search.search'))
        return render_template("login.html",error="用户不存在或密码错误。")  #省事
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for('search.search'))

@auth_bp.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not str(username).strip() or not str(password).strip():
            raise EmptyItem()
        if register_user(username,password):
            return redirect(url_for('auth.login'))
        else :
            return render_template("register.html",error="注册失败，请稍后再试。")
    return render_template("register.html")
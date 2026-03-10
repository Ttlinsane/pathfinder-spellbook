from flask import request,current_app,redirect,url_for,session
from functools import wraps
def get_keywords():
    kw = request.args.get("kw", "", type=str)
    # result per page
    rpp = request.args.get("rpp", current_app.config["ITEMS_PER_PAGE"], type=int)
    if rpp <= 0:
        rpp = 25
    if rpp >= 100:
        rpp = 100
    page = request.args.get("page", 1, type=int)
    if page <= 0:
        page = 1
    classMul = request.args.get("classMul")
    schoolMul = request.args.getlist("schoolMul")
    levelMul = request.args.getlist("levelMul")
    return {"kw":kw,"rpp":rpp,"page":page,"classMul":classMul,"schoolMul":schoolMul,"levelMul":levelMul}

def login_required(func):
    @wraps(func) #防装饰器改名
    def wrapper(*args,**kwargs):
        if "user" not in session:
            return redirect(url_for("search.search"))
        else:
            return func(*args,**kwargs)
    return wrapper
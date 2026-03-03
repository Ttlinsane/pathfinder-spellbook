from flask import request,current_app

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
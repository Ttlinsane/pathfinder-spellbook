from flask import Flask, request, g, render_template, Blueprint, current_app
import math
from db import get_db

search_bp = Blueprint('search',__name__)

@search_bp.route("/search")
def search():
    conn = get_db()
    cursor = conn.cursor()
    kw = request.args.get("kw",f"%%",type=str)
    #result per page
    rpp = request.args.get("rpp",current_app.config["ITEMS_PER_PAGE"],type=int)
    page = request.args.get("page",1,type=int)
    schoolMul = request.args.getlist("schoolMul")    
    offset = (page-1)*rpp
    #分开两个拼字符，算页码不得已而为之
    search_key = "SELECT * FROM spells WHERE "
    count_key ="SELECT COUNT(*) FROM spells WHERE "
    url_args = f"kw={kw}&rpp={rpp}"
    #这里也用列表方便干净
    params = []
    #想了想还是吧条件都先写上吧，大不了全选
    search_key += " (name LIKE ? OR description LIKE ? OR effect LIKE ?)"
    count_key += " (name LIKE ? OR description LIKE ? OR effect LIKE ?)"
    if not kw:
        params.extend([f"%%",f"%%",f"%%"])
    else:
        params.extend([f"%{kw}%",f"%{kw}%",f"%{kw}%"])
    if not schoolMul:
        schoolMul=["防护","咒法","预言","惑控","幻术","死灵","变化","塑能","通用"]
    for s in schoolMul:
        url_args += f"&schoolMul={s}"    
    placeholder = ",".join("?" for _ in schoolMul)
    search_key += f" AND school IN ({placeholder})"
    count_key += f" AND school IN ({placeholder})"
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
    return render_template("spell.html",kw=kw,page=page,rpp=rpp,results=row,ttp=ttp,url_args=url_args)

@search_bp.route("/search/<spell_name>")
def spell_detail(spell_name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spells WHERE name=? COLLATE NOCASE",(spell_name,))
    roww = cursor.fetchone()
    if roww:
        return render_template("spell_details.html",spell=roww)
    else:
        return render_template("spell.html", kw=spell_name, page=1, rpp=25, results=[], ttp=0, url_args="")
    
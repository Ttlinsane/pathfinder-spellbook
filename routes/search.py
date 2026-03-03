from flask import request, render_template, Blueprint, current_app
from db import get_info, get_details
from routes.helpers import get_keywords

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
def search():
    keywords = get_keywords()
    kw = keywords["kw"]
    rpp = keywords["rpp"]
    page = keywords["page"]
    classMul = keywords["classMul"]
    levelMul = keywords["levelMul"]
    schoolMul = keywords["schoolMul"]
    #此处可以用get_info(**keywords)解包使用，但需要注意需要返回参数名和字典key完全一致
    args = get_info(kw,page,rpp,classMul,levelMul,schoolMul)
    url_args = f"class={classMul}&kw={kw}&rpp={rpp}"
    """classMul,schoolMul,levelMul,kw,rpp"""
    if levelMul:
        for l in levelMul:
            url_args += f"&levelMul={l}"
    for s in schoolMul:
        url_args += f"&schoolMul={s}"
    return render_template(
        "spell.html", results=args["row"], ttp=args["ttp"], page=page, url_args=url_args
    )


@search_bp.route("/search/<spell_name>")
def spell_detail(spell_name):
    roww = get_details(spell_name)[0]
    if roww:
        return render_template("spell_details.html", spell=roww)
    else:
        return render_template(
            "spell.html", kw=spell_name, page=1, rpp=25, results=[], ttp=0, url_args=""
        )

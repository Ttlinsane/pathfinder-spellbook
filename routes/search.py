from flask import Flask, request, g, render_template, Blueprint, current_app
from db import get_info, get_details

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
def search():
    kw = request.args.get("kw", f"%%", type=str)
    # result per page
    rpp = request.args.get("rpp", current_app.config["ITEMS_PER_PAGE"], type=int)
    page = request.args.get("page", 1, type=int)
    classMul = request.args.get("classMul")
    schoolMul = request.args.getlist("schoolMul")
    levelMul = request.args.getlist("levelMul")
    args = get_info(kw, page, rpp, classMul, levelMul, schoolMul)
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
    roww = get_details(spell_name)
    if roww:
        return render_template("spell_details.html", spell=roww)
    else:
        return render_template(
            "spell.html", kw=spell_name, page=1, rpp=25, results=[], ttp=0, url_args=""
        )

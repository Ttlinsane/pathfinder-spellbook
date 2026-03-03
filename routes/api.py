from flask import Blueprint, jsonify, request, current_app
from db import get_info, get_details

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/spells")
def api_spell():
    kw = request.args.get("kw", "", type=str)
    # result per page
    rpp = request.args.get("rpp", current_app.config["ITEMS_PER_PAGE"], type=int)
    page = request.args.get("page", 1, type=int)
    classMul = request.args.get("classMul")
    schoolMul = request.args.getlist("schoolMul")
    levelMul = request.args.getlist("levelMul")
    args = get_info(kw, page, rpp, classMul, levelMul, schoolMul)
    # 返回的row里的东西是dict
    results = [dict(r) for r in args["row"]]
    # class c schools s levels l
    result_c = classMul
    result_s = [r for r in schoolMul]
    result_l = [r for r in levelMul]
    results_json = {
        # 先返回总数，在db里添加了返回值total
        "total": args["total"],
        "keyword": kw,
        "classMul": result_c,
        "schoolMul": result_s,
        "levelMul": result_l,
        "page": page,
        "rpp": rpp,
        "results": results,
    }
    return jsonify(results_json)


@api_bp.route("/spells/<spell_name>")
def spell_detail(spell_name):
    row = get_details(spell_name)
    result_json = {"error": "Spell not found"}
    if row:
        result_json = {
            "name": row["name"],
            "school": row["school"],
            "level": row["level_str"],
            "casting_time": row["casting_time"],
            "components": row["components"],
            "range_": row["range_"],
            "effect":row["effect"],
            "aiming":row["aiming"],
            "duration": row["duration"],
            "saving_throw": row["saving_throw"],
            "resistance": row["resistance"],
            "description": row["description"],
        }
        return jsonify(result_json)
    return jsonify(result_json),404
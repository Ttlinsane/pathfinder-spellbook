from flask import Blueprint, jsonify, request, current_app
from db import get_info, get_details
from routes.helpers import get_keywords

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/spells")
def api_spell():
    keywords = get_keywords()
    kw = keywords["kw"]
    rpp = keywords["rpp"]
    page = keywords["page"]
    classMul = keywords["classMul"]
    levelMul = keywords["levelMul"]
    schoolMul = keywords["schoolMul"]
    args = get_info(kw, page, rpp, classMul, levelMul, schoolMul)
    # 返回的row里的东西是dict
    results = [dict(r) for r in args["row"]]
    results_json = {
        # 先返回总数，在db里添加了返回值total
        "total": args["total"],
        "keyword": kw,
        "classMul": classMul,
        "schoolMul": schoolMul,
        "levelMul": levelMul,
        "page": page,
        "rpp": rpp,
        "results": results,
    }
    return jsonify(results_json),200


@api_bp.route("/spells/<spell_name>")
def spell_detail(spell_name):
    rows, rowl = get_details(spell_name)
    # 解包，解包！
    result_json = {"error": "Spell not found"}
    result_code = 404
    if rows:
        level_l = {i[0]: i[1] for i in rowl if i}
        result_json = {
            "name": rows["name"],
            "school": rows["school"],
            "level": level_l,
            "casting_time": rows["casting_time"],
            "components": rows["components"],
            "range_": rows["range_"],
            "effect": rows["effect"],
            "aiming": rows["aiming"],
            "duration": rows["duration"],
            "saving_throw": rows["saving_throw"],
            "resistance": rows["resistance"],
            "description": rows["description"],
        }
        result_code = 200
        return jsonify(result_json), result_code
    return jsonify(result_json), result_code
from flask import Blueprint, session, redirect, render_template, request, abort, g, redirect, url_for
from models import Authentication, Database, PageDetails, General,Tools
from functools import wraps
import ast
tools = Blueprint("tools", __name__)

@tools.route("/tools")
@tools.route("/tool")
def tools_index():
    ***REMOVED*** The Tools page ***REMOVED***
    posts_per_page = 9
    page = request.args.get("page")
    posts = Database().get_all_tools_data_db()
    last_page = len(posts)//posts_per_page
    if len(posts) - last_page*posts_per_page > 0:
        last_page+=1
    if page is None:
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            page = 1
    if page<1:
        return redirect("?page=1")
    limited_posts = (posts[(page-1)*posts_per_page:page*posts_per_page])
    if limited_posts == [] and page!=1:
        return redirect("?page={}".format(last_page))
    return render_template(
        "tools/tools_index.html",
        details=PageDetails(session).index_data(),
        posts=limited_posts,
        now_page=page,
        last_page=last_page,
        pagination=General().pagination_designer(page,last_page),
        days_till_now = General().days_passed_till_now(),

    )


@tools.route("/Tool/mbti" ,methods=["POST", "GET"])
@tools.route("/Tool/MBTI" ,methods=["POST", "GET"])
@tools.route("/Tool/16_personalities" ,methods=["POST", "GET"])
@tools.route("/tool/mbti" ,methods=["POST", "GET"])
@tools.route("/tool/MBTI" ,methods=["POST", "GET"])
@tools.route("/tool/16_personalities" ,methods=["POST", "GET"])
@tools.route("/tools/mbti" ,methods=["POST", "GET"])
@tools.route("/tools/MBTI" ,methods=["POST", "GET"])
@tools.route("/tools/16_personalities" ,methods=["POST", "GET"])
def mbti_test_tool():
    ***REMOVED*** The mbti 16personalities tool page. ***REMOVED***
    if request.method == "POST":
        all_answers = []
        for answer_index in range(1,60+1):
            answer = request.form.get(str(answer_index))
            if answer is None:
                return f"Quesion {answer_index} is not answered."
            all_answers.append(answer)
        user_mbti_answer = Tools().mbti_type_answer(all_answers)
        return redirect(url_for("tools.mbti_types_page", mbti_type=user_mbti_answer["final_type"], answer_percent=user_mbti_answer["answer_percent"] ))

    return render_template(
        "tools/mbti.html",
        details=PageDetails(session).index_data(),
        tool=Database().get_tool_data_db("16_personalities"),
        questions = General().open_json_file("static/tools/mbti.json")["questions"]
    )
    



@tools.route("/Tool/mbti/<mbti_type>" ,methods=["POST", "GET"])
@tools.route("/Tool/MBTI/<mbti_type>" ,methods=["POST", "GET"])
@tools.route("/Tool/16_personalities/<mbti_type>" ,methods=["POST", "GET"])
@tools.route("/tool/mbti/<mbti_type>" ,methods=["POST", "GET"])
@tools.route("/tool/MBTI/<mbti_type>" ,methods=["POST", "GET"])
@tools.route("/tool/16_personalities/<mbti_type>" ,methods=["POST", "GET"])
@tools.route("/tools/mbti/<mbti_type>" ,methods=["POST", "GET"])
@tools.route("/tools/MBTI/<mbti_type>" ,methods=["POST", "GET"])
@tools.route("/tools/16_personalities/<mbti_type>" ,methods=["POST", "GET"])
def mbti_types_page(mbti_type):
    ***REMOVED*** The mbti type page. ***REMOVED***
    user_mbti_type_upper = mbti_type.upper()
    answer_percent = request.args.get("answer_percent")
    if answer_percent is not None:
        answer_percent = (ast.literal_eval(answer_percent))
    if user_mbti_type_upper not in ['ESFJ','ESFP','ESTJ','ESTP','ENFJ','ENFP','ENTJ','ENTP','ISFJ','ISFP','ISTJ','ISTP','INFJ','INFP','INTJ','INTP']:
        return redirect(url_for("tools.mbti_test_tool"))
        
    user_mbti_answer = {'final_type': f'{user_mbti_type_upper}', 'answer_percent': answer_percent}
    return render_template(
        f"tools/mbti_base.html",
        details=PageDetails(session).index_data(),
        tool=Database().get_tool_data_db("16_personalities"),
        user_answer = user_mbti_answer,
        user_mbti_data =  General().open_json_file("static/tools/mbti.json")["mbti_types"][user_mbti_answer["final_type"]]
    )
    
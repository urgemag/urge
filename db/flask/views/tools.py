from flask import Blueprint, session, redirect, render_template, request, abort, g, redirect
from models import Authentication, Database, PageDetails, General
from functools import wraps

tools = Blueprint("tools", __name__)

@tools.route("/tools")
@tools.route("/tool")
def tools_index():
    ***REMOVED*** The Music page ***REMOVED***
    posts_per_page = 2
    page = request.args.get("page")
    posts = Database().get_tools_data_db()
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


@tools.route("/Tool/mbti")
@tools.route("/Tool/MBTI")
@tools.route("/tool/mbti")
@tools.route("/tool/MBTI")
@tools.route("/tools/mbti")
@tools.route("/tools/MBTI")
def mbti_test_tool():
    ***REMOVED*** The mbti 16personalities tool page. ***REMOVED***

    return render_template(
        "tools/mbti.html",
    )
    
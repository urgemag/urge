from flask import Blueprint, session, redirect, render_template, request, abort, g, redirect
from models import Authentication, Database, PageDetails, General
from functools import wraps

basic = Blueprint("basic", __name__)



def first_visit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            session["Visits"]
        except KeyError:
            session["Visits"] = {}

        try:
            session["Visits"]["index"]
            g.first_visit = False
        except KeyError:
            session["Visits"]["index"] = True
            g.first_visit = True

        return f(*args, **kwargs)

    return decorated


@basic.route("/")
@first_visit
def index():
    ***REMOVED*** The Dashboard ***REMOVED***
    return render_template(
        "basic/main.html", 
        details=PageDetails(session).index_data(),
        number_of_courses = PageDetails().number_of_courses(),
        top_courses = PageDetails().top_3_expensive_courses(),
        quotes = PageDetails().random_quotes(),
        random_blog_post = PageDetails().get_random_blog_post()
        )
    


@basic.route("/MotivationWall")
def motivational_sentences():
    ***REMOVED*** The motivational wall sentences page. ***REMOVED***

    # Handle if signed in
    if not Authentication(session).is_signed_in():
        return redirect("/LogIn")

    return render_template(
        "basic/motivationwall.html",
        details=PageDetails(session).motivation_wall_page_info_html(),
    )


from flask import Blueprint, session, redirect, render_template, request, abort, g, redirect
from models import Authentication, Database, PageDetails, General
from functools import wraps
from json import dumps
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
@basic.route("/Home")
@basic.route("/home")
@basic.route("/Dashboard")
@basic.route("/dashboard")
@first_visit
def index():
    ***REMOVED*** The Dashboard ***REMOVED***
    return render_template(
        "basic/main.html", 
        number_of_courses = PageDetails().number_of_courses(),
        top_courses = PageDetails().top_3_expensive_courses(),
        quotes = PageDetails().random_quotes(),
        random_blog_post = PageDetails().get_random_blog_post(),
        survey = PageDetails().get_survey_json_data()
        )

@basic.route("/survey",methods=["POST"])
@first_visit
def survey_topics():
    if session.get("logged_in"):
        identity = session["Data"]["Email"]
    else:
        identity = "unknown"
    user_ip_address = request.remote_addr
    request_args = request.get_json()
    topics = PageDetails().get_survey_json_data()["topics"]
    user_survey_answer = {}
    for topic in topics:
        user_survey_answer[topic] = request_args[topic]
    Database().add_user_survey_answer_to_db(
        user_ip_address,
        identity,
        dumps(user_survey_answer)
    )
    Authentication(session).user_answered_survey()
    return redirect("/")

    

@basic.route("/aboutus")
@basic.route("/Aboutus")
@basic.route("/AboutUs")
@basic.route("/about_us")
@basic.route("/About_us")
@basic.route("/About_Us")
@basic.route("/about-us")
@basic.route("/About-us")
@basic.route("/About-Us")
@basic.route("/us")
@basic.route("/Us")
@basic.route("/Us")
@basic.route("/urge")
@basic.route("/who-we-are")
@basic.route("/Who-We-Are")
@basic.route("/Who-Are-We")
@basic.route("/who-are-we")
@basic.route("/who_we_are")
@basic.route("/Who_We_Are")
@basic.route("/Who_Are_We")
@basic.route("/who_are_we")
@basic.route("/Urge")
@basic.route("/Urge")
def about_us():
    ***REMOVED*** The about us page. ***REMOVED***
    return render_template(
        "basic/about_us.html",
    )



@basic.route("/MotivationWall")
def motivational_sentences():
    ***REMOVED*** The motivational wall sentences page. ***REMOVED***

    # Handle if signed in
    if not Authentication(session).is_signed_in():
        return redirect("/LogIn")

    return render_template(
        "basic/motivationwall.html",
    )


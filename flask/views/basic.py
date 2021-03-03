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



def survey(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            survey_data_session = session["survey"]
        except KeyError:
            survey_data_session = 0
            session["survey"] = survey_data_session
            g.survey = True

        if type(survey_data_session) == int:
            if survey_data_session % 3 == 0:
                g.survey = True
            else:
                g.survey = False
            session["survey"] += 1 
        else:
            session["survey"] = 1

        return f(*args, **kwargs)

    return decorated


@basic.route("/")
@basic.route("/Home")
@basic.route("/home")
@basic.route("/Dashboard")
@basic.route("/dashboard")
@first_visit
@survey
def index():
    ***REMOVED*** The Dashboard ***REMOVED***
    return render_template(
        "basic/main.html", 
        details=PageDetails(session).index_data(),
        number_of_courses = PageDetails().number_of_courses(),
        top_courses = PageDetails().top_3_expensive_courses(),
        quotes = PageDetails().random_quotes(),
        random_blog_post = PageDetails().get_random_blog_post(),
        survey = PageDetails().get_survey_json_data()
        )

@basic.route("/survey",methods=["POST", "GET"])
@first_visit
def survey_topics():
    if request.method == "POST":
        request_args = request.get_json()
        topics = PageDetails().get_survey_json_data()["topics"]
        user_survey_answer = {}
        for topic in topics:
            user_survey_answer[topic] = request_args[topic]
        return str(user_survey_answer)

    return render_template(
        "basic/survey.html", 
        details=PageDetails(session).index_data(),
        number_of_courses = PageDetails().number_of_courses(),
        top_courses = PageDetails().top_3_expensive_courses(),
        quotes = PageDetails().random_quotes(),
        random_blog_post = PageDetails().get_random_blog_post(),
        survey = PageDetails().get_survey_json_data()
        )
    

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
        details=PageDetails(session).index_data(),
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


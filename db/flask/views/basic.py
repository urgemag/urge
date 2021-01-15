from flask import Blueprint, session, redirect, render_template, request, abort, g
from models import Authentication, Database, PageDetails, General
from functools import wraps

basic = Blueprint("basic", __name__)


def check_is_admin():
    def _check_is_admin(f):
        @wraps(f)
        def __check_is_admin(*args, **kwargs):
            result = f(*args, **kwargs)
            if not Authentication(session).is_admin():
                abort(401)
            return result

        return __check_is_admin

    return _check_is_admin


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
    ***REMOVED*** The Dashboard - Also Check if not a member , redirect to /SignUp page. ***REMOVED***
    return render_template(
        "basic/main.html", 
        details=PageDetails(session).index_data(),
        number_of_courses = PageDetails().number_of_courses(),
        top_courses = PageDetails().top_3_expensive_courses(),
        quotes = PageDetails().random_quotes()
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


@basic.route("/uploader/ck/day&responseType=json", methods=["POST", "GET"])
@check_is_admin()
def upload_test():
    ***REMOVED*** The Upload Api. ***REMOVED***
    if request.method == "POST":

        uploaded_image = request.files.get("upload")
        uploaded_image_bytes = uploaded_image.read()

        hash_image = General().sha256_hash_bytes(uploaded_image_bytes)

        format_file = General().format_recognizer(uploaded_image_bytes)
        file_name = "day_of_course_" + str(hash_image) + "." + format_file
        location_image = "static/assets/images/days_of_course/" + file_name

        with open(location_image, "wb") as file:
            file.write(uploaded_image_bytes)

        General().image_resizer_using_imgp(location_image)
        General().logo_merger(location_image)
        General().image_optimizer_using_imgp(location_image)
        width, height = General().size_image_file(image_path=location_image)
        return {
            "uploaded": 1,
            "fileName": file_name,
            "url": "/static//assets/images/days_of_course/" + file_name,
            "width": width,
            "height": height,
        }

    return ""

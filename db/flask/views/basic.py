from flask import Blueprint, session, redirect, render_template, request, abort, g, redirect
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
    ***REMOVED*** The Dashboard ***REMOVED***
    return render_template(
        "basic/main.html", 
        details=PageDetails(session).index_data(),
        number_of_courses = PageDetails().number_of_courses(),
        top_courses = PageDetails().top_3_expensive_courses(),
        quotes = PageDetails().random_quotes(),
        random_blog_post = PageDetails().get_random_blog_post()
        )
    

@basic.route("/blog")
def blog():
    ***REMOVED*** The Blog ***REMOVED***
    posts_per_page = 2
    page = request.args.get("page")
    posts = Database().get_blog_posts_data_from_db()
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
        "basic/blog_posts.html", 
        details=PageDetails(session).index_data(),
        posts=limited_posts,
        days_passed_till_now = General().days_passed_till_now(),
        milliseconds_passed_till_now = General().milliseconds_passed_till_now(),
        now_page=page,
        last_page=last_page,
        pagination=General().pagination_designer(page,last_page)
        )
    
@basic.route("/blog/<english_name>")
def blog_post(english_name):
    ***REMOVED*** One post from Blog ***REMOVED***
    post = Database().get_blog_post_data_from_db(english_name)
    if post is False:
        abort(404)
    return render_template(
        "basic/blog_post.html", 
        details=PageDetails(session).index_data(),
        posts=Database().get_blog_posts_data_from_db(),
        postss=Database().get_blog_posts_data_from_db(),
        days_passed_till_now = General().days_passed_till_now(),
        post=post
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
def upload_day_pic_ck():
    ***REMOVED*** The Upload day Api. ***REMOVED***
    if request.method == "POST":
        #slug = request.args.get('slug')
        #day = int(request.args.get('day'))
        #if Database().get_courses_data_from_db(slug) is False:
        #    abort(400)

        uploaded_image = request.files.get("upload")
        uploaded_image_bytes = uploaded_image.read()

        saved_picture_data = General().save_picture_of_day_of_course_not_in_specific_location(uploaded_image_bytes)

        location_image = saved_picture_data["image"]
        file_name = saved_picture_data["file_name"]
        location_image_href = saved_picture_data["href"]
        
        width, height = General().size_image_file(image_path=location_image)
        return {
            "uploaded": 1,
            "fileName": file_name,
            "url": location_image_href,
            "width": width,
            "height": height,
        }

    return ""



@basic.route("/uploader/ck/blog&responseType=json", methods=["POST", "GET"])
@check_is_admin()
def upload_blog_pic_ck():
    ***REMOVED*** The Upload blog Api. ***REMOVED***
    if request.method == "POST":

        uploaded_image = request.files.get("upload")
        uploaded_image_bytes = uploaded_image.read()

        hash_image = General().sha256_hash_bytes(uploaded_image_bytes)

        format_file = General().format_recognizer(uploaded_image_bytes)
        file_name = "post_blog_" + str(hash_image) + "." + format_file
        location_image = "static/assets/images/ck_cache/" + file_name
        location_image_href = "/static//assets/images/ck_cache/" + file_name

        with open(location_image, "wb") as file:
            file.write(uploaded_image_bytes)

        General().image_resizer_using_imgp(location_image)
        General().logo_merger(location_image)
        General().image_optimizer_using_imgp(location_image)
        width, height = General().size_image_file(image_path=location_image)
        return {
            "uploaded": 1,
            "fileName": file_name,
            "url": location_image_href,
            "width": width,
            "height": height,
        }

    return ""
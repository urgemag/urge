from flask import Blueprint, session, redirect, render_template, request, abort, g, redirect
from models import Authentication, Database, PageDetails, General
from functools import wraps

blog = Blueprint("blog", __name__)

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


@blog.route("/blog")
def blog_index():
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
        "blog/blog_posts.html", 
        details=PageDetails(session).index_data(),
        posts=limited_posts,
        days_passed_till_now = General().days_passed_till_now(),
        milliseconds_passed_till_now = General().milliseconds_passed_till_now(),
        now_page=page,
        last_page=last_page,
        pagination=General().pagination_designer(page,last_page)
    )
    
@blog.route("/blog/<english_name>")
def blog_post(english_name):
    ***REMOVED*** One post from Blog ***REMOVED***
    post = Database().get_blog_post_data_from_db(english_name)
    if post is False:
        abort(404)
    return render_template(
        "blog/blog_post.html", 
        details=PageDetails(session).index_data(),
        posts=Database().get_blog_posts_data_from_db(),
        postss=Database().get_blog_posts_data_from_db(),
        days_passed_till_now = General().days_passed_till_now(),
        post=post
        )



@blog.route("/uploader/ck/blog&responseType=json", methods=["POST", "GET"])
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
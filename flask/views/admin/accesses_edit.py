from flask import Blueprint, session, redirect, render_template, request, flash, url_for,abort
from models import PageDetails, Database, General, Authentication
from functools import wraps

admin_edit = Blueprint("admin_edit", __name__)

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


@admin_edit.route("/Admin/Edit/Post", methods=["POST", "GET"])
@admin_edit.route("/Admin/Remove/Post", methods=["POST", "GET"])
@check_is_admin()
def post_blog_options_admin():
    ***REMOVED*** The edit/remove a Post for blog options Page as an admin. ***REMOVED***

    return render_template(
        "admin/admin_edit_remove_post_options.html",
        posts=Database().get_blog_posts_data_from_db(),
        days_passed_till_now = General().days_passed_till_now()
    )


@admin_edit.route("/Admin/Edit/Post/<slug_post>", methods=["POST", "GET"])
@check_is_admin()
def edit_post_blog_admin(slug_post):
    ***REMOVED*** The edit a Post for blog Page as an admin. ***REMOVED***
    post = Database().get_blog_post_data_from_db(slug_post)
    if post is False:
        abort(404)
    if request.method == "POST":

        def form_handler(request):
            slug = request.form.get("name_eng")
            if request.form.get("name_persian") == "":
                return {"Result": False, "Message": "نام فارسی دوره را وارد کنید."}
            if request.form.get("name_eng") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("text") == "":
                return {"Result": False, "Message": "متن اصلی را وارد کنید."}
            uploaded_file = request.files["cover"]
            if uploaded_file.filename != "":

                english_name = slug
                uploaded_image = request.files.get("cover")
                uploaded_image_bytes = uploaded_image.read()
                format_file = General().format_recognizer(uploaded_image_bytes)
                General().setup_blog_post_folder(slug)
                file_name = "blog-cover_" + english_name + "." + format_file
                location_image = "static/assets/images/blog/{}/".format(slug) + file_name
                location_image_href = "/static//assets/images/blog/{}/".format(slug) + file_name
                with open(location_image, "wb") as file:
                    file.write(uploaded_image_bytes)
                General().image_resizer_using_imgp(location_image, 1500)
                General().image_optimizer_using_imgp(location_image)
            else:
                location_image_href = post["Cover"]
            
            message = Database().edit_post_blog_to_db(
                old_enlish_name=slug_post,
                persian_name=request.form.get("name_persian"),
                eng_name=(request.form.get("name_eng").replace(" ","-")).replace("_","-"),
                cover_href=location_image_href,
                text=request.form.get("text"),
            )
            return message,(request.form.get("name_eng").replace(" ","-")).replace("_","-")

        message,eng_slug = form_handler(request)
        message_original = message
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت ویرایش شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        print (message)
        if message_original is True:
            return redirect('/blog/{}'.format(eng_slug))
        else:
            return redirect('/Admin/Edit/Post/{}'.format(post["English_Name"]))


    return render_template(
        "admin/admin_edit_post.html",
        post=post,
        days_passed_till_now = General().days_passed_till_now()
    )
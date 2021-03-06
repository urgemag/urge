from flask import Blueprint, session, redirect, render_template, request, flash, url_for, abort
from models import PageDetails, Database,Authentication, General
from functools import wraps

admin_remove = Blueprint("admin_remove", __name__)


@admin_remove.route("/Admin/Remove", methods=["POST", "GET"])
@admin_remove.route("/Admin/remove", methods=["POST", "GET"])
@admin_remove.route("/Admin/Delete", methods=["POST", "GET"])
@admin_remove.route("/Admin/delete", methods=["POST", "GET"])
def admin_remove_index():
    return render_template("admin/admin_remove_options.html")


@admin_remove.route("/Admin/Remove/Day-Part", methods=["POST", "GET"])
def remove_day_options_admin():
    """ The Remove day options Page as an admin. """

    if request.method == "POST":

        def form_handler(request):

            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            remove_ones = []
            day_parts = [
                "Name",
                "Cover",
                "Description",
                "Text",
                "To_Do",
                "Quotes",
                "Musics",
                "Musics_Description",
                "Ted_Video",
                "Ted_Video_Description",
                "Animation_Link",
                "Animation_Description",
                "Movie_Links",
                "Movie_Text",
                "Movie_Cover",
                "Podcast",
                "Podcast_Description",
            ]
            for part in day_parts:
                if (part) == request.form.get(part):
                    remove_ones.append(part)

            message = Database().delete_parts_of_day_of_course_data_in_db(
                slug=request.form.get("slug"),
                day_of_course=request.form.get("day"),
                remove_parts_names=remove_ones,
            )
            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت حذف شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_options_admin"))

    Parts = PageDetails().all_day_parts_to_remove_in_admin_page()

    return render_template(
        "admin/admin_remove_day_options.html",
        Parts=Parts,
        Courses=PageDetails(session).all_courses_page_info_html(),
    )

@admin_remove.route("/Admin/Remove/Course", methods=["POST", "GET"])

def remove_course_admin():
    """ The Remove day options Page as an admin. """

    if request.method == "POST":

        def form_handler(request):

            remove_ones = []
            course_names = []
            for course in PageDetails().all_courses_page_info_html():
                course_names.append(course["Slug"])
            for part in course_names:
                if (part) == request.form.get(part):
                    remove_ones.append(part)

            for course in remove_ones: 
                Database().delete_courses_data_from_db(course)
                General().remove_file_to_trash("static/assets/images/blog/{slug}/".format(slug=course))

                
            return True

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت حذف شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_course_admin"))

    Parts = PageDetails().all_course_data_slug_name_to_remove_in_admin_page()

    return render_template(
        "admin/admin_remove_courses.html",
        Parts=Parts,
    )


@admin_remove.route("/Admin/Remove/Day", methods=["POST", "GET"])

def remove_full_day_admin():
    """ The Remove Full Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):

            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().delete_day_of_course_data_to_db(
                slug=request.form.get("slug"),
                day=request.form.get("day"),
            )
            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت حذف شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_full_day_admin"))

    Parts = PageDetails().all_day_parts_to_remove_in_admin_page()

    return render_template(
        "admin/admin_remove_day.html",
        Parts=Parts,
        Courses=PageDetails(session).all_courses_page_info_html(),
    )


@admin_remove.route("/Admin/Remove/Day/Essential", methods=["POST", "GET"])

def remove_day_essential_main_data_admin():
    """ The Remove Essential Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_essential_main_data_admin"))

    return render_template(
        "admin/admin_remove_day_essential.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_remove.route("/Admin/Remove/Day/Text", methods=["POST", "GET"])

def remove_day_text_data_admin():
    """ The Remove Main Text Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_text_data_admin"))

    return render_template(
        "admin/admin_remove_day_text.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_remove.route("/Admin/Remove/Day/Todo", methods=["POST", "GET"])

def remove_day_todo_data_admin():
    """ The Remove Todo-Excersices Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_todo_data_admin"))

    return render_template(
        "admin/admin_remove_day_todo.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_remove.route("/Admin/Remove/Day/Quotes", methods=["POST", "GET"])

def remove_day_quotes_data_admin():
    """ The Remove Quotes Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_quotes_data_admin"))

    return render_template(
        "admin/admin_remove_day_quotes.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_remove.route("/Admin/Remove/Day/Music", methods=["POST", "GET"])

def remove_day_music_data_admin():
    """ The Remove Music Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_music_data_admin"))

    return render_template(
        "admin/admin_remove_day_music.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_remove.route("/Admin/Remove/Day/Ted", methods=["POST", "GET"])

def remove_day_ted_data_admin():
    """ The Remove TED video Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_ted_data_admin"))

    return render_template(
        "admin/admin_remove_day_ted.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_remove.route("/Admin/Remove/Day/Animation", methods=["POST", "GET"])

def remove_day_animation_data_admin():
    """ The Remove short Animation film Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_animation_data_admin"))

    return render_template(
        "admin/admin_remove_day_animation.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_remove.route("/Admin/Remove/Day/Podcast", methods=["POST", "GET"])

def remove_day_podcast_data_admin():
    """ The Remove podcast Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_podcast_data_admin"))

    return render_template(
        "admin/admin_remove_day_podcast.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_remove.route("/Admin/Remove/Day/Movie", methods=["POST", "GET"])

def remove_day_movie_data_admin():
    """ The Remove Movie Day Page as an admin. """
    if request.method == "POST":

        def form_handler(request):
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}

            message = Database().add_delete_day_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
            )

            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_day_movie_data_admin"))

    return render_template(
        "admin/admin_remove_day_movie.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )

@admin_remove.route("/Admin/Remove/Post/<slug_post>", methods=["POST", "GET"])

def remove_post_blog_admin(slug_post):
    """ The remove a Post for blog Page as an admin. """
    post = Database().get_blog_post_data_from_db(slug_post)
    if post is False:
        abort(404)
        
    if request.method == "POST":
        def form_handler(request):
            if request.form.get("confirmation") == "True":
                message = Database().delete_post_blog_data_from_db(slug_post)
            else:
                message = {"Result": False, "Message": "حذف تایید نشده است."}
            General().remove_file_to_trash("static/assets/images/blog/{slug}/".format(slug=slug_post))
            return message

        message = form_handler(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت حذف شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_edit.post_blog_options_admin"))


    return render_template(
        "admin/admin_remove_post.html",
        post=post
    )


@admin_remove.route("/Admin/Remove/Music", methods=["POST", "GET"])

def remove_music_admin():
    """ The Remove Music as an admin. """

    if request.method == "POST":

        def form_handler(request):
            name = request.form.get("music_name")

            remove_ones = []
            music_names = []
            for music_name in Database().get_all_musics_data_from_db():
                music_names.append(music_name["Music_Name"])
            for part in music_names:
                if (part) == request.form.get(part):
                    remove_ones.append(part)

            for music_name in remove_ones: 
                Database().delete_music_data_from_db(music_name)

            message = True
            return message

        message = form_handler(request)

        if message is True:
            message = {"Color": "green", "Result": "با موفقیت حذف شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_music_admin"))

    Parts = PageDetails().all_music_data_name_creator_to_remove_in_admin_page()
    return render_template(
        "admin/admin_remove_musics.html",
        Parts=Parts,
    )



@admin_remove.route("/Admin/Remove/Tool", methods=["POST", "GET"])
@admin_remove.route("/Admin/Remove/tool", methods=["POST", "GET"])

def remove_tool_admin():
    """ The Remove tool as an admin. """

    if request.method == "POST":

        def form_handler(request):
            name = request.form.get("tool_name")

            remove_ones = []
            tool_names = []
            for tool_name in Database().get_all_tools_data_db():
                tool_names.append(tool_name["Slug"])
            for part in tool_names:
                if part == request.form.get(part):
                    remove_ones.append(part)

            for tool_slug in remove_ones: 
                Database().delete_tool_data_from_db(tool_slug)

            message = True
            return message

        message = form_handler(request)

        if message is True:
            message = {"Color": "green", "Result": "با موفقیت حذف شد."}
        else:
            if message["Result"] is False:
                message["Color"] = "red"
            else:
                message["Color"] = "green"
            message["Result"] = message["Message"]

        flash(message)
        return redirect(url_for("admin_remove.remove_tool_admin"))

    Parts = PageDetails().all_tools_data_name_slug_to_remove_in_admin_page()
    return render_template(
        "admin/admin_remove_tool.html",
        Parts=Parts,
    )
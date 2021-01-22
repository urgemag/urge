from flask import Blueprint, session, redirect, render_template, request, flash, url_for,abort
from models import PageDetails, Database, General, Authentication
from functools import wraps

admin_add = Blueprint("admin_add", __name__)

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

@admin_add.route("/Admin/Add/User", methods=["POST", "GET"])
@check_is_admin()
def add_user_admin():
    ***REMOVED*** The Add User Page as an admin. ***REMOVED***

    message = False
    if request.method == "POST":
        accesses = []
        for course in Database().get_all_slug_and_names_of_courses_from_db():
            if (course["Slug"]) == request.form.get(course["Slug"]):
                accesses.append(course["Slug"])
        message = Database().add_users_data_to_db(
            email=request.form.get("email"),
            password=General().sha256_hash(request.form.get("password")),
            first_name=request.form.get("name"),
            last_name=request.form.get("last_name"),
            phone_number=request.form.get("phone_num"),
            about_me=request.form.get("about_me"),
            bio=request.form.get("bio"),
            website=request.form.get("web"),
            birth_day=request.form.get("day"),
            birth_month=request.form.get("month"),
            birth_year=request.form.get("year"),
            Accesses=accesses,
        )
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            message["Result"] = message["Message"]
            message["Color"] = "red"

        flash(message)
        return redirect(url_for("admin_add.add_user_admin"))

    return render_template(
        "admin/admin_add_user.html",
        Accesses=PageDetails().all_accesses_admin_page(),
        message=message,
    )


@admin_add.route("/Admin/Add/Day", methods=["POST", "GET"])
@check_is_admin()
def add_day_options_admin():
    ***REMOVED*** The Add options Page as an admin. ***REMOVED***

    return render_template(
        "admin/admin_add_day_options.html",
    )


@admin_add.route("/Admin/Add/Day/Essential", methods=["POST", "GET"])
@check_is_admin()
def add_day_essential_main_data_admin():
    ***REMOVED*** The Add Essential Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):

            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if request.form.get("name_day") == "":
                return {"Result": False, "Message": "اسم روز را وارد کنید."}
            if request.form.get("description") == "":
                return {"Result": False, "Message": "توضیحات روز را وارد کنید."}
            if (
                request.form.get("price-status") != "None-Free"
                and request.form.get("price-status") != "Free"
            ):
                return {
                    "Result": False,
                    "Message": "اطلاعات مربوط به هزینه صحیح وارد نشده است.",
                }
            if request.form.get("price-status") == "None-Free":
                freeness = False
            else:
                freeness = True

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}
            try:
                uploaded_file = request.files["cover"]
            except:
                return {"Result": False, "Message": "تصویر را آپلود کنید."}
            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            uploaded_image = request.files.get("cover")
            uploaded_image_bytes = uploaded_image.read()

            hash_image = General().sha256_hash_bytes(uploaded_image_bytes)

            format_file = General().format_recognizer(uploaded_image_bytes)
            file_name = "day_of_course_" + str(hash_image) + "." + format_file
            location_image = "static/assets/images/days_of_course/" + file_name
            location_image_href = "/static//assets/images/days_of_course/" + file_name
            with open(location_image, "wb") as file:
                file.write(uploaded_image_bytes)

            General().image_resizer_using_imgp(location_image, 700)
            General().image_optimizer_using_imgp(location_image)

            href = "/static//assets/images/days_of_course/" + file_name

            message = Database().add_day_essential_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                name_persian=request.form.get("name_day"),
                description=request.form.get("description"),
                image_path=location_image_href,
                freeness=freeness,
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
        return redirect(url_for("admin_add.add_day_essential_main_data_admin"))

    return render_template(
        "admin/admin_add_day_essential.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Day/Text", methods=["POST", "GET"])
@check_is_admin()
def add_day_text_data_admin():
    ***REMOVED*** The Add Main Text Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):

            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if request.form.get("text") == "":
                return {"Result": False, "Message": "متن اصلی را وارد کنید."}

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().add_day_text_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                text=request.form.get("text"),
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
        return redirect(url_for("admin_add.add_day_text_data_admin"))

    return render_template(
        "admin/admin_add_day_text.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Day/Todo", methods=["POST", "GET"])
@check_is_admin()
def add_day_todo_data_admin():
    ***REMOVED*** The Add Todo-Excersices Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):

            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if request.form.get("todo") == "":
                return {"Result": False, "Message": "تمارین را وارد کنید."}

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().add_day_todo_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                todo=request.form.get("todo"),
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
        return redirect(url_for("admin_add.add_day_text_data_admin"))

    return render_template(
        "admin/admin_add_day_todo.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Day/Quotes", methods=["POST", "GET"])
@check_is_admin()
def add_day_quotes_data_admin():
    ***REMOVED*** The Add Quotes Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):

            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if list(filter(None, request.form.getlist("quote"))) == []:
                return {"Result": False, "Message": "نقل قول ها را وارد کنید."}
            quotes = list(filter(None, request.form.getlist("quote")))
            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().add_day_quotes_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                quotes=quotes,
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
        return redirect(url_for("admin_add.add_day_quotes_data_admin"))

    return render_template(
        "admin/admin_add_day_quotes.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Day/Music", methods=["POST", "GET"])
@check_is_admin()
def add_day_music_data_admin():
    ***REMOVED*** The Add Music Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):
            covers = request.files.getlist("cover")
            musics = request.files.getlist("music")
            creators = request.form.getlist("creator")
            names = request.form.getlist("music_name")
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if request.form.get("description") == "":
                return {"Result": False, "Message": "توضیحات موزیک را وارد کنید."}

            for music in musics:
                if music.filename == "":
                    musics.remove(music)

            for cover in covers:
                if cover.filename == "":
                    covers.remove(cover)

            for name in names:
                if name == "":
                    names.remove(name)

            for creator in creators:
                if creator == "":
                    creators.remove(creator)

            if creators == [] or names == []:
                return {"Result": False, "Message": "اطلاعات موزیک را وارد کنید."}
            if musics == [] or covers == []:
                return {
                    "Result": False,
                    "Message": "مدیاهای مربوط به موزیک را وارد کنید.",
                }
            if not (
                len(covers) == len(musics)
                and len(musics) == len(creators)
                and len(creators) == len(names)
            ):
                return {"Result": False, "Message": "همه فیلد های موزیک را وارد کنید."}

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().add_day_musics_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                description=request.form.get("description"),
                covers=covers,
                musics=musics,
                creators=creators,
                names=names,
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
        return redirect(url_for("admin_add.add_day_music_data_admin"))

    return render_template(
        "admin/admin_add_day_music.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Day/Ted", methods=["POST", "GET"])
@check_is_admin()
def add_day_ted_data_admin():
    ***REMOVED*** The Add TED video Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):
            urls = request.form.getlist("ted_url")
            qualities = request.form.getlist("ted_quality")
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if request.form.get("description") == "":
                return {"Result": False, "Message": "توضیحات ویدیوها را وارد کنید."}

            for url in urls:
                if url == "":
                    urls.remove(url)

            for quality in qualities:
                if quality == "":
                    qualities.remove(quality)

            if urls == [] or qualities == []:
                return {"Result": False, "Message": "لینک و یا کیفیت ها را وارد کنید."}
            if not (len(urls) == len(qualities)):
                return {"Result": False, "Message": "همه فیلد های ویدیو را وارد کنید."}

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().add_day_ted_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                description=request.form.get("description"),
                urls=urls,
                qualities=qualities,
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
        return redirect(url_for("admin_add.add_day_ted_data_admin"))

    return render_template(
        "admin/admin_add_day_ted.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Day/Animation", methods=["POST", "GET"])
@check_is_admin()
def add_day_animation_data_admin():
    ***REMOVED*** The Add short Animation film Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):
            urls = request.form.getlist("animation_url")
            qualities = request.form.getlist("animation_quality")
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if request.form.get("description") == "":
                return {"Result": False, "Message": "توضیحات ویدیو را وارد کنید."}

            for url in urls:
                if url == "":
                    urls.remove(url)

            for quality in qualities:
                if quality == "":
                    qualities.remove(quality)

            if urls == [] or qualities == []:
                return {"Result": False, "Message": "لینک و یا کیفیت ها را وارد کنید."}
            if not (len(urls) == len(qualities)):
                return {
                    "Result": False,
                    "Message": "همه فیلد های انیمیشن را وارد کنید.",
                }

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().add_day_animation_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                description=request.form.get("description"),
                urls=urls,
                qualities=qualities,
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
        return redirect(url_for("admin_add.add_day_animation_data_admin"))

    return render_template(
        "admin/admin_add_day_animation.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Day/Podcast", methods=["POST", "GET"])
@check_is_admin()
def add_day_podcast_data_admin():
    ***REMOVED*** The Add podcast Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):
            creator = request.form.get("creator")
            name = request.form.get("podcast_name")
            cover = request.files.get("cover")
            url = request.form.get("podcast_url")
            if creator == "" or name == "":
                return {"Result": False, "Message": "اطلاعات پادکست را وارد کنید."}
            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if request.form.get("description") == "":
                return {"Result": False, "Message": "توضیحات پادکست را وارد کنید."}
            if url == "":
                return {"Result": False, "Message": "لینک پادکست را وارد کنید."}
            if cover.filename == "":
                return {"Result": False, "Message": "کاور پادکست را وارد کنید."}

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().add_day_podcast_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                description=request.form.get("description"),
                url=url,
                cover=cover,
                creator=creator,
                name=name,
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
        return redirect(url_for("admin_add.add_day_podcast_data_admin"))

    return render_template(
        "admin/admin_add_day_podcast.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Day/Movie", methods=["POST", "GET"])
@check_is_admin()
def add_day_movie_data_admin():
    ***REMOVED*** The Add Movie Day Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_handler(request):
            cover = request.files.get("cover")
            urls = request.form.getlist("movie_url")
            qualities = request.form.getlist("movie_quality")

            if request.form.get("slug") == "":
                return {"Result": False, "Message": "نام انگلیسی دوره را وارد کنید."}
            if request.form.get("day") == "":
                return {"Result": False, "Message": "روز دوره را وارد کنید."}
            if request.form.get("description") == "":
                return {"Result": False, "Message": "توضیحات پادکست را وارد کنید."}
            if cover.filename == "":
                return {"Result": False, "Message": "کاور پادکست را وارد کنید."}

            for url in urls:
                if url == "":
                    urls.remove(url)

            for quality in qualities:
                if quality == "":
                    qualities.remove(quality)

            if urls == [] or qualities == []:
                return {"Result": False, "Message": "لینک و یا کیفیت ها را وارد کنید."}
            if not (len(urls) == len(qualities)):
                return {"Result": False, "Message": "همه فیلد ها را وارد کنید."}

            try:
                int(request.form.get("day"))
            except ValueError:
                return {"Result": False, "Message": "روز دوره باید عدد باشد."}

            if Database().get_courses_data_from_db(request.form.get("slug")) is False:
                return {"Result": False, "Message": "همچین دوره ای وجود ندارد."}

            message = Database().add_day_movie_data_to_db(
                course_name_slug=request.form.get("slug"),
                day_num=request.form.get("day"),
                description=request.form.get("description"),
                urls=urls,
                qualities=qualities,
                cover=cover,
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
        return redirect(url_for("admin_add.add_day_movie_data_admin"))

    return render_template(
        "admin/admin_add_day_movie.html",
        Courses=Database().get_all_slug_and_names_of_courses_from_db(),
    )


@admin_add.route("/Admin/Add/Course", methods=["POST", "GET"])
@check_is_admin()
def add_course_admin():
    ***REMOVED*** The Add Course Page as an admin. ***REMOVED***

    if request.method == "POST":

        def form_course(request):
            if request.form.get("slug") == "":
                return {"Message": "نام انگلیسی دوره را وارد کنید."}
            try:
                uploaded_file = request.files["cover"]
            except:
                print("hrer")
                return {"Message": "تصویر را آپلود کنید."}
            if (
                Database().get_courses_data_from_db(request.form.get("slug")) != ""
                and uploaded_file.filename == ""
            ):
                return {"Message": "تصویر را آپلود کنید."}
            result_pic = General().save_picture_of_course(
                request.form.get("slug"), uploaded_file
            )
            if result_pic["Result"] is False:
                return result_pic
            if request.form.get("price-status") == "Free":
                price = "0"
                free = True
            else:
                price = request.form.get("price")
                free = False
            if request.form.get("soon") == "Soon":
                soon = True
            else:
                soon = False

            try:
                int(request.form.get("len"))
            except ValueError:
                General().remove_file(result_pic["path"])
                return {"Color": "red", "Message": "طول دوره باید عدد باشد."}
            try:
                if request.form.get("soon") == "Soon":
                    days_till_open = int(request.form.get("date_open"))
                else:
                    days_till_open = 0
            except ValueError:
                General().remove_file(result_pic["path"])
                return {"Color": "red", "Message": "فاصله زمانی تا باز شدن باید عدد باشد."}
            try:
                int(price.replace(",", ""))
            except ValueError:
                General().remove_file(result_pic["path"])
                return {"Color": "red", "Message": "قیمت دوره باید عدد باشد."}

            message = Database().add_course_data_to_db(
                name=request.form.get("name"),
                slug=request.form.get("slug"),
                description=request.form.get("description"),
                intro=None,
                image_href=result_pic["href"],
                now_price=int(price.replace(",", "")),
                length_of_course=int(request.form.get("len")),
                robbin=request.form.get("robbin"),
                free=free,
                soon=soon,
                published_date=General().days_passed_till_now()+days_till_open
            )
            if message is not True:
                General().remove_file(result_pic["path"])
            return message

        message = form_course(request)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            message["Result"] = message["Message"]
            message["Color"] = "red"
        flash(message)
        return redirect(url_for("admin_add.add_course_admin"))

    return render_template(
        "admin/admin_add_course.html",
    )


@admin_add.route("/Admin/Add/Course-Info", methods=["POST", "GET"])
@check_is_admin()
def add_course_info_admin():
    ***REMOVED*** The Add Course information Page as an admin. ***REMOVED***

    if request.method == "POST":
        print("-------------")
        print(request.form.get("slug"))
        print("-------------")
        message = Database().add_course_info_to_db(
            slug=request.form.get("slug"),
            introduction=request.form.get("intro"),
            speciality=request.form.get("speciality"),
            importance=request.form.get("importance"),
            why=request.form.get("why"),
            length=request.form.get("length"),
            price=request.form.get("price"),
            last_words=request.form.get("last_word"),
        )
        print(message)
        if message is True:
            message = {"Color": "green", "Result": "با موفقیت اضافه شد."}
        else:
            message["Result"] = message["Message"]
            message["Color"] = "red"
        flash(message)
        return redirect(url_for("admin_add.add_course_info_admin"))

    return render_template(
        "admin/admin_add_course_info.html",
        Courses=PageDetails().get_all_courses_info_categorized_by_info_existence(),
    )

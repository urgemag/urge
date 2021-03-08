from flask import Blueprint, session, redirect, render_template, abort, url_for, request, g
from models import Database, General, PageDetails,Authentication
from suds.client import Client
import setting
from functools import wraps

courses_and_days = Blueprint("courses_and_days", __name__)


MMERCHANT_ID =  setting.mmerchant_id
ZARINPAL_WEBSERVICE = setting.zarinpal_webservice
description = u'بخش پرداخت و خرید دوره از سایت انگیزشی Urge'

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


def log_in_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        g.is_signed_in = Authentication(session).is_signed_in()
            
        return f(*args, **kwargs)
    return decorated


@courses_and_days.route("/Courses")
def all_courses():
    """ The Courses page. """
    courses_per_page = 10
    courses = PageDetails(session).all_courses_list()
    courses.reverse()
    page = request.args.get("page")
    last_page = len(courses)//courses_per_page
    if len(courses) - last_page*courses_per_page > 0:
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
    limited_courses = (courses[(page-1)*courses_per_page:page*courses_per_page])
    if limited_courses == [] and page!=1:
        return redirect("?page={}".format(last_page))

    try:
        identity = session["Data"]["Email"]
    except KeyError:
        identity = ""

    return render_template(
        "courses_and_days/courses.html",
        courses=limited_courses,
        accesses=Database().get_users_access_data_from_db(identity),
        days_till_now = General().days_passed_till_now(),
        now_page=page,
        last_page=last_page,
        pagination=General().pagination_designer(page,last_page)
    )


@courses_and_days.route("/Course/<slug>/info")
def info_course(slug):
    """ The one Course info page. """

    data = PageDetails().info_intro_course_page(slug)
    if data is False or "Intro" not in data:
        return redirect(url_for("courses_and_days.one_course", slug= slug))
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    return render_template(
        "courses_and_days/course_info.html",
        course=data,
    )


@courses_and_days.route("/Course/<slug>")
def one_course(slug):
    """ The one Course page. """
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        identity = ""
    data = PageDetails().course_page_info(slug)
    if data is False:
        abort(404)
    
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    return render_template(
        "courses_and_days/course.html",
        course=data[0],
        days=data[1],
        intro=data[2],
        accesses=Database().get_users_access_data_from_db(identity),
        days_till_now = General().days_passed_till_now()
    )
    
@courses_and_days.route("/Course/<slug>/buy")
@log_in_auth
def cart(slug):
    """ The Course Buy page. """
    data = PageDetails().course_page_info(slug)
    if data is False:
        abort(404)
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        identity = ""
    if slug in Database().get_users_access_data_from_db(identity) or data[0]["Free"] is True or data[0]["Now_Price"] == 0:
        return redirect("/Course/{slug}/start".format(slug=slug))
    
    return render_template(
        "courses_and_days/cart.html",
        course=data[0],
        days=data[1],
        intro=data[2],
    )

@courses_and_days.route("/Course/<slug>/start")
@log_in_auth
def start_free_course(slug):
    """ The free Course start page. """
    data = PageDetails().course_page_info(slug)
    if data is False:
        abort(404)
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        identity = ""
    if slug in Database().get_users_access_data_from_db(identity):
        return redirect("/Course/{slug}".format(slug=slug))
    if not (slug in Database().get_users_access_data_from_db(identity) or data[0]["Free"] is True or data[0]["Now_Price"] == 0):
        return redirect("/Course/{slug}/buy".format(slug=slug))
    
    return render_template(
        "courses_and_days/start_course_card.html",
        course=data[0],
        days=data[1],
        intro=data[2],
    )
    
@courses_and_days.route("/Course/<slug>/buy/success")
def success_page_course(slug):
    """ The Course Buy report success page. """
    data = PageDetails().course_page_info(slug)
    if data is False:
        abort(404)
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        identity = ""
        
    if slug not in Database().get_users_access_data_from_db(identity):
        return redirect("/Course/{slug}".format(slug=slug))
    try: code= (request.args['auth_code'])
    except KeyError: return redirect("/Course/{slug}".format(slug=slug))
    return render_template(
        "courses_and_days/success_payment.html",
        course=data[0],
        days=data[1],
        intro=data[2],
        code=code
    )
@courses_and_days.route("/Course/<slug>/buy/fail")
def fail_page_course(slug):
    """ The Course Buy report fail page. """
    data = PageDetails().course_page_info(slug)
    if data is False:
        abort(404)
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        identity = ""
        
    if slug not in Database().get_users_access_data_from_db(identity):
        return redirect("/Course/{slug}".format(slug=slug))
    try: code= (request.args['auth_code'])
    except KeyError: return redirect("/Course/{slug}".format(slug=slug))
    return render_template(
        "courses_and_days/fail_payment.html",
        course=data[0],
        days=data[1],
        intro=data[2],
        code=code
        
    )
    
@courses_and_days.route("/Course/<slug>/start/success")
def success_page_course_start(slug):
    """ The Course start success page. """
    data = PageDetails().course_page_info(slug)
    if data is False:
        abort(404)
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        identity = ""
        
    if slug not in Database().get_users_access_data_from_db(identity):
        return redirect("/Course/{slug}".format(slug=slug))

    return render_template(
        "courses_and_days/success_start.html",
        course=data[0],
        days=data[1],
        intro=data[2],
    )
    
@courses_and_days.route("/Course/<slug>/buy/redirect")
def buy_course_redirect(slug):
    """ The Course redirect to zarinpall page. """
    data = PageDetails().course_page_info(slug)
    if data is False:
        abort(404)
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        return redirect("/LogIn")
        
    if slug in Database().get_users_access_data_from_db(identity):
        return redirect("/Course/{slug}".format(slug=slug))
    
    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(MMERCHANT_ID,
                                           int(str(data[0]["Now_Price"]).replace(",", "")),
                                           description,
                                           'email',
                                           "mobile",
                                           str(url_for('courses_and_days.buy_callback', _external=True)))

    if result.Status == 100:
        Database().add_payment_record_to_db(slug,data[0]["Now_Price"],identity,str(result.Authority))
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return 'Error'

@courses_and_days.route("/Course/<slug>/start/redirect")
def start_course_redirect(slug):
    """ The Course redirect to start the free course page. """
    data = PageDetails().course_page_info(slug)
    if data is False:
        abort(404)
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        return redirect("/LogIn")
        
    if slug in Database().get_users_access_data_from_db(identity):
        return redirect("/Course/{slug}".format(slug=slug))
    
    Database().add_users_access_data_to_db(identity,slug)
    return redirect("/Course/{slug}/start/success".format(slug=slug))
    

@courses_and_days.route("/Course/buy/callback/")
def buy_callback():
    """ The Course callback page from zarinpall page. """
    client = Client(ZARINPAL_WEBSERVICE)
    
    payment_data = Database().get_payment_data(str(request.args['Authority']))
    
    if request.args.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.args['Authority'],
                                                    int(str(payment_data["Price"]).replace(',', '')))
        if result.Status == 100 or result.Status == 101:
            Database().add_users_access_data_to_db(payment_data["Buyer"],payment_data["Slug"])
            Database().change_payment_status_to_success_in_db(str(request.args['Authority']))
            return redirect("/Course/{slug}/buy/success?auth_code={code}".format(slug=payment_data["Slug"],code=str(request.args['Authority'])))
        
        else:
            Database().change_payment_status_to_fail_in_db(str(request.args['Authority']))
            return redirect("/Course/{slug}/buy/fail?auth_code={code}".format(slug=payment_data["Slug"],code=str(request.args['Authority'])))

            
    else:
        Database().change_payment_status_to_fail_in_db(str(request.args['Authority']))
        return redirect("/Course/{slug}/buy/fail?auth_code={code}".format(slug=payment_data["Slug"],code=str(request.args['Authority'])))
        




@courses_and_days.route("/Course/<slug>/<day>")
def sub_course(slug, day):
    """ The one sub Course page. """
    # Day is a number or not
    try:
        day = int(day)
    except ValueError:
        abort(404)
    course = Database().get_courses_data_from_db(slug)
    published_date = General().convert_timestamp_to_days(course["First_Created_TimeStamp"]) + course["Days_Till_Open"]
    if published_date > General().days_passed_till_now():
        abort(404)
    try:
        identity = session["Data"]["Email"]
    except KeyError:
        identity = ""

    # Get needed Data
    course_data = Database().get_courses_data_from_db(slug=slug)
    day_data = Database().get_one_day_data_of_courses_data_from_db(slug, day)

    # Check Length Day
    if int(day) > int(course_data["Length"]):
       return redirect("/Course/{}".format(slug))

    # Check if data is FALSE or not
    if course_data is False or day_data is False:
        abort(404)

    # Some days and courses in database might not have "Free" key, so we add them.
    if "Free" not in day_data:
        day_data["Free"] = False
    if "Free" not in course_data:
        course_data["Free"] = False

    # Check if day or course is not free and if we do not have access
    user_accesses = Database().get_users_access_data_from_db(identity)
    if (
        course_data["Free"] is not True
        and slug not in user_accesses
        and day_data["Free"] is False
    ):
        return redirect("/Course/{}/info".format(slug))

    if slug in user_accesses and (user_accesses[slug]-1+day- General().days_passed_till_now()) > 0:
        return redirect("/Course/{}".format(slug))

    return render_template(
        "courses_and_days/day.html",
        course=PageDetails(session).course_page_info(slug)[0],
        day=PageDetails(session).sub_course_page_info_html(slug, day),
    )


@courses_and_days.route("/uploader/ck/day&responseType=json", methods=["POST", "GET"])
@check_is_admin()
def upload_day_pic_ck():
    """ The Upload day Api. """
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

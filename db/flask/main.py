***REMOVED***The main***REMOVED***
from flask import Flask, g, session, url_for, redirect, render_template
import setting
from flask_recaptcha import ReCaptcha
from models import General, Authentication, Database, PageDetails
from flask_dance.contrib.google import make_google_blueprint, google
from os import environ

# importing views
from views.auths import auths
from views.basic import basic
from views.courses_and_days import courses_and_days
from views.errors import errors
from views.user import user
from views.admin.accesses_add import admin_add
from views.admin.accesses_remove import admin_remove
from views.admin.accesses_edit import admin_edit
from views.blog import blog
from views.music import music
from views.tools import tools
from flask_analytics import Analytics

# end of importing views
from logging import FileHandler, WARNING, CRITICAL, ERROR


file_handler_warning_logs = FileHandler("log/logs-warning.txt")
file_handler_warning_logs.setLevel(ERROR)

file_handler_critical_logs = FileHandler("log/logs-critical.txt")
file_handler_critical_logs.setLevel(ERROR)

file_handler_error_logs = FileHandler("log/logs-error.txt")
file_handler_error_logs.setLevel(ERROR)

app = Flask(
    __name__,
    template_folder=setting.template_folder,
    static_folder=setting.static_folder,
)

Analytics(app)
app.config['ANALYTICS']['GAUGES']['SITE_ID'] = 'G-4QTVXWX8LF'

app.logger.addHandler(file_handler_error_logs)
app.logger.addHandler(file_handler_critical_logs)
app.logger.addHandler(file_handler_warning_logs)
app.jinja_env.globals.update(status_date_published_post_blog=General().status_date_published_post_blog)
app.jinja_env.globals.update(convert_timestamp=General().convert_timestamp)
app.jinja_env.globals.update(smart_description_preview_splitted_by_word=General().smart_description_preview_splitted_by_word)
app.jinja_env.globals.update(price_beautifier=General().price_beautifier)
app.jinja_env.globals.update(html_to_text=General().html_to_text)
app.secret_key = setting.secret_key
app.config["DEBUG"] = setting.debug_mode
app.config.update(
    {
        "RECAPTCHA_ENABLED": setting.recaptcha_enabled,
        "RECAPTCHA_DATA_ATTRS": {"theme": setting.recaptcha_theme},
        "RECAPTCHA_SITE_KEY": setting.recaptcha_public_key,
        "RECAPTCHA_SECRET_KEY": setting.recaptcha_secret_key,
    }
)
recaptcha = ReCaptcha(app=app)
# registering blueprints
for blueprint in (auths,courses_and_days,errors,user,admin_add,admin_remove,admin_edit,blog,music,tools):
    app.register_blueprint(blueprint)










# Things that need to be at main because they need >app< to be able to be ran 

environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
client_id = setting.google_client_id
client_secret = setting.google_client_secret


google_oauth_blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    offline=True,
    scope=["profile", "email"],

)

app.register_blueprint(google_oauth_blueprint, url_prefix="/login")

from functools import wraps
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


@app.route("/")
@app.route("/Home")
@app.route("/home")
@app.route("/Dashboard")
@app.route("/dashboard")
@first_visit
def index():
    ***REMOVED*** The Dashboard ***REMOVED***
    if not Authentication(session).is_signed_in():
        if google.authorized:
            resp = google.get("/oauth2/v2/userinfo")
            assert resp.ok, resp.text
            email = resp.json()["email"]
            first_name = resp.json()["given_name"].capitalize() 
            last_name = resp.json()["family_name"].capitalize() 
            cover = resp.json()["picture"]
            if Authentication().is_user_account_registered(email) is False:
                Database().add_users_data_to_db(email=email, first_name=first_name, last_name=last_name, cover=cover, password=0, registered_with="Google")

            session["Data"] = {"Email": General().corect_form_of_email(email)}
            session.permanent = True
            session["logged_in"] = True          

    return render_template(
        "basic/main.html", 
        details=PageDetails(session).index_data(),
        number_of_courses = PageDetails().number_of_courses(),
        top_courses = PageDetails().top_3_expensive_courses(),
        quotes = PageDetails().random_quotes(),
        random_blog_post = PageDetails().get_random_blog_post()
        )
    

@app.route("/log-in/google")
@app.route("/log-in_google")
@app.route("/Log-in/google")
@app.route("/Log-In/google")
@app.route("/log-in/Google")
@app.route("/log-in_Google")
@app.route("/Log-in/Google")
@app.route("/Log-In/Google")
@app.route("/sign-in/google")
@app.route("/sign-in_google")
@app.route("/Sign-in/google")
@app.route("/Sign-In/google")
@app.route("/sign-in/Google")
@app.route("/sign-in_Google")
@app.route("/Sign-in/Google")
@app.route("/Sign-In/Google")
def google_login():
    if not Authentication(session).is_signed_in():
        if not google.authorized:
            return redirect(url_for("google.login"))
    return redirect(url_for("auths.logout"))



@app.route("/LogOutRequest")
def logout_form():
    ***REMOVED*** The Logout request. ***REMOVED***

    # Handle if signed in
    if not Authentication(session).is_signed_in():
        return redirect("/LogIn")

    session["logged_in"] = False
    session["admin"] = False

    try:
        del app.blueprints['google'].token
    except KeyError:
        pass
    return redirect("/")



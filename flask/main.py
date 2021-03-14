"""The main"""
from flask import Flask, g, session, abort, render_template, request, redirect
from flask_compress import Compress
import setting
from flask_recaptcha import ReCaptcha
from models import General, PageDetails, Authentication

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

app.config["COMPRESS_REGISTER"] = True  # disable default compression of all eligible requests
compress = Compress()
compress.init_app(app)

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
def essential_user_details():
    if request.full_path.endswith(".jpg?") or not request.full_path.startswith("/static"):
        g.details = PageDetails(session).index_data()

def survey_data():
    if not request.full_path.startswith("/static"):

        if Authentication(session).has_user_answered_survey() is True:
            g.survey = False
        else:
            try:
                survey_data_session = session["survey"]
            except KeyError:
                survey_data_session = 0
                session["survey"] = survey_data_session
                g.survey = True
            if type(survey_data_session) == int:
                if survey_data_session % 6 == 0:
                    g.survey = True
                else:
                    g.survey = False
                session["survey"] += 1 
            else:
                g.survey = True
                session["survey"] = 1
            
        g.survey_data = PageDetails().get_survey_json_data()

def check_is_admin():
    if not request.full_path.startswith("/static"):
        if not Authentication(session).is_admin():
            abort(401)

def is_it_admin():
    if not request.full_path.startswith("/static"):
        g.is_admin = Authentication(session).is_admin()

def is_it_production_mode():
    if not request.full_path.startswith("/static"):
        g.production = setting.production

def fix_extra_slash_at_the_end_of_the_url():
    print(request.full_path)
    if request.full_path.count("/") != 1 and request.full_path.endswith("/?"):
        return redirect(request.full_path[0:-2])

admin_add.before_request(check_is_admin)
admin_edit.before_request(check_is_admin)
admin_remove.before_request(check_is_admin)
app.before_request(essential_user_details)
app.before_request(survey_data)
app.before_request(is_it_production_mode)
app.before_request(is_it_admin)
app.before_request(fix_extra_slash_at_the_end_of_the_url)
# registering blueprints
for blueprint in (auths,basic,courses_and_days,errors,user,admin_add,admin_remove,admin_edit,blog,music,tools):
    app.register_blueprint(blueprint)


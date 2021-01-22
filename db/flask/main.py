***REMOVED***The main***REMOVED***
from flask import Flask
import setting
from flask_recaptcha import ReCaptcha
from models import General
# importing views
from views.auths import auths
from views.basic import basic
from views.courses_and_days import courses_and_days
from views.errors import errors
from views.user import user
from views.admin.accesses_add import admin_add
from views.admin.accesses_remove import admin_remove
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
app.logger.addHandler(file_handler_error_logs)
app.logger.addHandler(file_handler_critical_logs)
app.logger.addHandler(file_handler_warning_logs)

app.jinja_env.globals.update(price_beautifier=General().price_beautifier)
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
for blueprint in (auths,basic,courses_and_days,errors,user,admin_add,admin_remove):
    app.register_blueprint(blueprint)


from flask import Blueprint, render_template, session
from models import PageDetails
from werkzeug.exceptions import HTTPException

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(HTTPException)
def not_found(e):
    ***REMOVED*** The 404 not found page. ***REMOVED***
    print ("---------------------")
    return render_template("errors/error.html",
        details = PageDetails(session).index_data(),
        error_code = str(e.code)
    )

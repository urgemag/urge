from flask import Blueprint

errors = Blueprint("errors", __name__)


@errors.errorhandler(404)
def not_found(e):
    ***REMOVED*** The 404 not found page. ***REMOVED***

    # return render_template("404.html")
    return "404"

import requests
from flask import Blueprint, session, redirect, render_template, request, abort
from models import Authentication
import setting
import json

auths = Blueprint("auths", __name__)


@auths.route("/LogIn")
def login():
    """ The LogIn Page - Send Form to /LogInFormPost . """

    if Authentication(session).is_signed_in():
        return redirect("/")

    return render_template("auths/signin.html")


@auths.route("/LogInFormPost", methods=["POST"])
def login_form():
    """ The Login Data Form Post Api. """

    try:
        recaptcha_request = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": setting.recaptcha_secret_key,
                "response": request.form["g-recaptcha-response"],
            },
        )

        google_response = json.loads(recaptcha_request.text)
        username_or_email = request.form.get("email")
        password = request.form.get("password")

    # Handle Wrong Form Data
    except KeyError:
        abort(400)

    # Handle Wrong ReCaptcha
    if not google_response["success"]:
        return render_template(
            "auths/signin.html", message=" لطفا 'من ربات نیستم' را انجام دهید. "
        )

    # Handle Wrong Username or password
    sign_in_data = Authentication().signin(username_or_email, password)
    if not sign_in_data["result"]:
        return render_template("auths/signin.html", message=sign_in_data["message"])

    # Set Up a sesson , make it permanent ,
    session["Data"] = sign_in_data["session"]
    session.permanent = True
    session["logged_in"] = True
    if username_or_email == "admin@admin.com":
        session["admin"] = True
    else:
        session["admin"] = False
        
    return redirect("/")


@auths.route("/SignUp")
def signup():
    """ The SignUp Page - Send Form to /SignUpFormPost . """

    if Authentication(session).is_signed_in():
        return redirect("/")

    return render_template("auths/signup.html")


@auths.route("/SignUpFormPost", methods=["POST"])
def signup_form():
    """ The Login Data Form Post Api. """

    try:
        recaptcha_request = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": "6LfokdYZAAAAALgHTMNJ9vIZws16wKtlF7-529tW",
                "response": request.form["g-recaptcha-response"],
            },
        )

        google_response = json.loads(recaptcha_request.text)
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

    # Handle Wrong Form Data
    except KeyError:
        abort(400)

    # Handle Wrong ReCaptcha
    if not google_response["success"]:
        return render_template(
            "auths/signup.html", message='  "من ربات نیستم" را انجام دهید '
        )

    # Handle Wrong signup info
    sign_up_data = Authentication().signup(first_name, last_name, email, password)
    if not sign_up_data["result"]:
        return render_template("auths/signup.html", message=sign_up_data["message"])

    # Set Up a sesson , make it permanent ,
    session["Data"] = sign_up_data["session"]
    session.permanent = True
    session["logged_in"] = True

        

    return redirect("/")


@auths.route("/LogOut")
def logout():
    """ The LogOut submit Page - Send request to /SignUpFormPost . """

    if not Authentication(session).is_signed_in():
        return redirect("/")

    return render_template("auths/logout.html")


@auths.route("/LogOutRequest")
def logout_form():
    """ The Logout request. """

    # Handle if signed in
    if not Authentication(session).is_signed_in():
        return redirect("/LogIn")

    session["logged_in"] = False
    session["admin"] = False

    return redirect("/")

from flask import Blueprint, session, redirect, render_template, request
from models import Authentication, Database, PageDetails

user = Blueprint("user", __name__)


@user.route("/Profile")
def profle():
    ***REMOVED*** The Profile page. ***REMOVED***

    # Handle if signed in
    if not Authentication(session).is_signed_in():
        return redirect("/LogIn")

    return render_template(
        "user/profile.html"
    )


@user.route("/ProfileSetting")
def profle_setting():
    ***REMOVED*** The Profile setting page. ***REMOVED***

    # Handle if signed in
    if not Authentication(session).is_signed_in():
        return redirect("/LogIn")

    return render_template(
        "user/profile_setting.html"
    )


@user.route("/ProfileSettingUpdate", methods=["POST"])
def profile_change_form():
    ***REMOVED*** The Profile Data update or change Form Post Api. ***REMOVED***

    # Handle Form Data
    name = request.form.get("name")
    phone_number = request.form.get("phone_number")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    email = request.form.get("email")

    profile_change_form_result = Database().edit_users_data_from_db(
        session["Data"]["Email"],
        {
            "name": name,
            "phone_number": phone_number,
            "old_password": old_password,
            "new_password": new_password,
            "email": email,
        },
    )

    return render_template(
        "user/profile_setting.html", message=profile_change_form_result["message"]
    )


@user.route("/UrgeMails")
def urge_mails():
    ***REMOVED*** The Mail page. ***REMOVED***

    # Handle if signed in
    if not Authentication(session).is_signed_in():
        return redirect("/LogIn")

    return render_template(
        "user/mail.html"
    )

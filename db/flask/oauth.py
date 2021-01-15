import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

client_id = "266736865296-rh5sudd5sv8rmgqjl8m4p67d406aek1o"
client_secret = "4yRJOV35ozZT720s4VQZZDOi"

from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    offline=True,
    scope=["profile", "email"],
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    return render_template("_.html")


@app.route("/welcome")
def welcome():

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json()["email"]

    return str(email)


@app.route("/login/google")
def login():
    if not google.authorized:
        return render_template(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json()["email"]

    return str(email)


if __name__ == "__main__":
    app.run(port=4444)

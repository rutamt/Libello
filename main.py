"""Python Flask WebApp Auth0 integration example
"""

import time
from urllib import response
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

import os
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import (
    Flask,
    redirect,
    render_template,
    session,
    url_for,
    request,
    flash,
)
import schoolopy
import requests
from functools import wraps
from flask_talisman import Talisman

from auth0_utils import AUTH0_DOMAIN, CLIENT_ID, CLIENT_SECRET, Auth0Utils
from misc_utils import check_if_duplicates, get_assignments

SCHOOLOGY_API_KEY = os.environ.get("SCHOOLOGY_API_KEY")
SCHOOLOGY_API_SECRET = os.environ.get("SCHOOLOGY_API_SECRET")
HOSTNAME = os.environ.get("HOSTNAME")
SCHOOLOGY_DOMAIN = "https://henrico.schoology.com"

app = Flask(__name__)
Talisman(app, content_security_policy=None)
app.secret_key = os.environ.get("APP_SECRET_KEY")
oauth = OAuth(app)

auth0 = Auth0Utils()

auth = schoolopy.Auth(
    consumer_key=SCHOOLOGY_API_KEY,
    consumer_secret=SCHOOLOGY_API_SECRET,
    three_legged=True,
    domain=SCHOOLOGY_DOMAIN,
)

oauth.register(
    "auth0",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def is_logged_in():
    ret_val = False
    user_info = session.get("user", {}).get("userinfo")
    if user_info:
        ret_val = True
    return ret_val


def login_required(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        # check if user is logged in
        if not is_logged_in():
            # print("User was not logged in. :(")
            return render_template("401.html"), 401
        # they were logged in, so go ahead
        return func(*args, **kwargs)

    return _inner


# Controllers API
@app.route("/")
def home():
    # print("home()")
    return render_template(
        "index.html",
        session=session.get("user"),
        is_logged_in=is_logged_in(),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    # print("callback()")
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/work")


@app.route("/login")
def login():
    # print("login()")
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    # print("logout()")
    session.clear()
    return redirect(
        f"https://{AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )


@app.route("/auth")
@login_required
def schoology_auth():

    user_info = session.get("user")["userinfo"]
    creds = auth0.get_user_creds(user_info)
    if creds != ["default", "default"]:
        return redirect(url_for("work"))

    url = auth.request_authorization(callback_url="libello.herokuapp.com/work")
    if url is None:
        return "URL NOT NONE"
    return render_template("3leggedsignin.html", url=url, is_logged_in=is_logged_in())


@app.route("/work")
@login_required
def work():
    def get_url3():
        access_token = auth.access_token
        access_token_secret = auth.access_token_secret
        # print(f"GET_URL3: KEY:{access_token}, SECRET: {access_token_secret}")
        user_info = session.get("user")["userinfo"]
        # print("AUTH0.UPDATE USER CALLING")
        auth0.update_user(
            user_info=user_info, key=access_token, secret=access_token_secret
        )

    # print("work()")

    # # print("Session in /work", session)
    user_info = session.get("user")["userinfo"]
    # print("USER INFO:", session.get("user")["userinfo"])
    try:
        name = session.get("user")["userinfo"]["given_name"]
    except KeyError:
        name = session.get("user")["userinfo"]["nickname"]

    # name = session.get("user")["userinfo"]["given_name"]
    classes = auth0.get_user_classes(user_info)
    creds = auth0.get_user_creds(user_info)

    if not creds or creds == ["default", "default"]:

        # check if we got creds from an oauth 3-legged workflow
        # print("auth access tokens are", auth.access_token, auth.access_token_secret)
        # print("Running auth.authorize()")
        auth.authorize()

        if auth.access_token and auth.access_token_secret:
            # print("RUNNING GET_URL3")
            get_url3()
        else:
            # print("NOT CREDS")
            return redirect(url_for("schoology_auth"))

    if not classes or classes == "default":
        # print("NOT CLASSES")
        return render_template(
            "planner.html",
            is_logged_in=is_logged_in(),
            name=f"{name}",
            classes=None,
            creds="YES",
        )
    else:
        # print(f"WORK GOING TO ELSE, creds: {creds}, classes {classes}")
        assignments = get_assignments(
            key=creds[0], secret=creds[1], classes=classes.split(",")
        )
        if not assignments:
            # print("Invalid token/secret")
            return redirect(url_for("schoology_auth"))

        # # print(f"ASSIGNMENTS {assignments}")
        # print("Everything works")
        return render_template(
            "planner.html",
            is_logged_in=is_logged_in(),
            assignments=assignments,
            name=name,
            creds="YES",
            classes="YES",
        )


@app.route("/setup", methods=["GET", "POST"])
@login_required
def setup():
    # print("setup()")

    user_info = session.get("user", {}).get("userinfo")
    if not user_info:
        # print("Could not find the user that is logged on :(")
        return redirect(url_for("work"))

    creds = auth0.get_user_creds(user_info=user_info)
    if not creds:
        flash("Please enter your API KEY and SECRET first")
        return render_template("setup.html", is_logged_in=is_logged_in(), classes=[])

    if request.method == "POST":
        if not request.form.getlist("classes"):
            return render_template(
                "setup.html",
                is_logged_in=is_logged_in(),
            )
        else:
            values = request.form.getlist("classes")
            # print(values)

            if check_if_duplicates(values):
                flash("Please remove duplicate class ids")
                return render_template(
                    "setup.html", is_logged_in=is_logged_in(), classes=[]
                )
            else:
                try:
                    # flash("Checking that the class IDs are valid.", category="info")
                    # print("Checking if class IDs are valid")
                    get_assignments(key=creds[0], secret=creds[1], classes=values)
                except requests.exceptions.HTTPError:
                    # print("Invalid class IDs ")
                    flash("Invalid class ids", category="error")
                    return render_template(
                        "setup.html", is_logged_in=is_logged_in(), classes=[]
                    )
                else:
                    # flash("Saving your class IDs.", category="info")
                    # print("Saving your class IDs.")
                    auth0.update_user(user_info=user_info, _class=",".join(values))
                    return redirect(url_for("work"))

    # this for HTTP method GET
    classes = auth0.get_user_classes(user_info=user_info).split(",")
    if classes == [""]:
        classes = []
    return render_template(
        "setup.html",
        classes=classes,
        is_logged_in=is_logged_in(),
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        is_logged_in=is_logged_in(),
    )


# https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="localhost", port=os.environ.get("PORT", 3000))

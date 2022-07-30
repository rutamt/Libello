"""Python Flask WebApp Auth0 integration example
"""

from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

import json
import os
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, session, url_for, request, flash
import schoolopy
import datetime
import requests

from auth0_utils import AUTH0_DOMAIN, CLIENT_ID, CLIENT_SECRET, Auth0Utils
from misc_utils import check_if_duplicates, get_assignments

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")
oauth = OAuth(app)

auth0 = Auth0Utils()

oauth.register(
    "auth0",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration',
)

def is_logged_in():
    ret_val = False
    user_info = session.get("user", {}).get("userinfo")
    if user_info:
        ret_val = True
    return ret_val

# Controllers API
@app.route("/")
def home():
    print("home()")
    return render_template(
        "index.html",
        session=session.get("user"),
        is_logged_in=is_logged_in(),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    print("callback()")
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/work")


@app.route("/login")
def login():
    print("login()")
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    print("logout()")
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




@app.route('/work')
def work():
    print("work()")
    print("Session in /work", session)
    user_info = session.get("user")['userinfo']

    name = session.get("user")['userinfo']['given_name']
    classes = auth0.get_user_classes(user_info)
    creds = auth0.get_user_creds(user_info)

    time = datetime.datetime.now().strftime('%A %B %d, %Y')

    if not creds or not classes:
        return render_template("planner.html", is_logged_in=is_logged_in(), time=time, name=f"{name}", classes="NONE")
    else:
        assignments = get_assignments(key=creds[0], secret=creds[1], classes=classes.split(','))
        return render_template("planner.html", is_logged_in=is_logged_in(), time=time, assignments=assignments, name=name)


@app.route('/setup', methods=["GET", "POST"])
def setup():
    print("setup()")

    user_info = session.get("user", {}).get("userinfo")
    if not user_info:
        print("Could not find the user that is logged on :(")
        return redirect(url_for('work'))

    creds = auth0.get_user_creds(user_info=user_info)
    if not creds:
        print("Please enter your API KEY and SECRET first")
        return render_template("setup.html", is_logged_in=is_logged_in(), classes=[])

    if request.method == "POST":
        if not request.form.getlist('classes'):
            return render_template("setup.html", is_logged_in=is_logged_in(),)
        else:
            values = request.form.getlist('classes')
            print(values)

            if check_if_duplicates(values):
                flash("Please remove duplicate class ids")
                return redirect(url_for('setup'))
            else:
                try:
                    # flash("Checking that the class IDs are valid.", category="info")
                    get_assignments(key=creds[0], secret=creds[1], classes=values)
                except requests.exceptions.HTTPError:
                    flash('Invalid class ids', category="error")
                    return redirect(url_for("work"))
                else:
                    # flash("Saving your class IDs.", category="info")
                    print("Saving your class IDs.")
                    auth0.update_user(user_info=user_info, _class=",".join(values))
                    return redirect(url_for("work"))

    # this for HTTP method GET
    classes = auth0.get_user_classes(user_info=user_info).split(",")
    if classes == [""]:
        classes = []
    return render_template("setup.html", classes=classes, is_logged_in=is_logged_in(),)


@app.route('/register', methods=["GET", "POST"])
def register():
    print("register()")

    if request.method == "POST":
        key = request.form.get('key')
        secret = request.form.get('secret')
        if not key or not secret:
            flash("You must provide key and secret.", category="error")
            return redirect(url_for("register"))

        try:
            sc = schoolopy.Schoology(schoolopy.Auth(key, secret))
            sc.get_me()

        except requests.exceptions.HTTPError:
            flash('Invalid api key/secret', category="error")
            return redirect(url_for("register"))

        else:
            print("SUCCESS")
            user_info = session.get("user")["userinfo"]
            auth0.update_user(user_info=user_info, key=key, secret=secret)
            return redirect(url_for("work"))

    # this is for HTTP method GET
    return render_template("register.html", is_logged_in=is_logged_in(),)


@app.route('/about')
def about():
    return render_template("about.html", is_logged_in=is_logged_in(),)


if __name__ == "__main__":
    app.run(host="localhost", port=os.environ.get("PORT", 3000), debug=True)

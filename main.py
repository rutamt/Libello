"""Python Flask WebApp Auth0 integration example
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
import schoolopy
import datetime

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Controllers API
@app.route("/")
def home():
    return render_template(
        "index.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/work")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

def get_assignments(key="1de57784114df33651b1af7ec0d35fdf0625b5cbb", secret="89b44b05a27ebed1dc3a96b8d434627a", classes = None):

    # Create a Schoology instance with Auth as a parameter.

    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))


    if classes is None:
        return "NONE"
    else:
        cl_list = []

        for i in classes:
            cl_list += (sc.get_assignments(i))
        return cl_list


@app.route('/work')
def work():
    time = datetime.datetime.now().strftime('%A %B %d, %Y')
    name = "TEST"
    # if current_user.classes == None:
    #     return render_template("planner.html", time=time,  name=name, classes="NONE")

    # return render_template("setup.html", classes=(current_user.classes).split(","))
    assignments = get_assignments(classes = ("5167125116, 5167125194").split(","))
    return render_template("planner.html", time=time, assignments=assignments, name=name)

@app.route('/about')
def about():
    return render_template("about.html")
if __name__ == "__main__":
    app.run(host="localhost", port=env.get("PORT", 3000), debug=True)

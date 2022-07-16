from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import requests
import datetime
import schoolopy
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv


if os.environ.get("PG_URL") is None:
    load_dotenv()

PG_URL = os.environ.get("PG_URL")

def get_assignments(key, secret, classes = None):

    # Create a Schoology instance with Auth as a parameter.

    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))


    if classes is None:
        return "NONE"
    else:
        cl_list = []

        for i in classes:
            cl_list += (sc.get_assignments(i))
        return cl_list


app = Flask(__name__)

encrypt_key = Fernet.generate_key()
fernet = Fernet(encrypt_key)

flask_key = os.urandom(12)

app.config['SECRET_KEY'] = flask_key
app.config['SQLALCHEMY_DATABASE_URI'] = PG_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


def check_if_duplicates(list_of_elems):
    """Check if given list contains any duplicates

    Credit: https://thispointer.com/python-3-ways-to-check-if-there-are-duplicates-in-a-list/
    """
    set_of_elems = set()
    for elem in list_of_elems:
        if elem in set_of_elems:
            return True
        else:
            set_of_elems.add(elem)
    return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    key = db.Column(db.String(41))
    secret = db.Column(db.String(32))
    classes = db.Column(db.String(1000))
#Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    # Every render_template has a logged_in variable set.
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            get_assignments(key=request.form.get('key'), secret=request.form.get('secret'))
        except requests.exceptions.HTTPError:
            flash('invalid api key/secret')
            return redirect(url_for("register"))
        else:
            if User.query.filter_by(email=request.form.get('email')).first():
                # User already exists
                flash("You've already signed up with that email, log in instead!")
                return redirect(url_for('login'))

            hash_and_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                name=request.form.get('name'),
                email=request.form.get('email'),
                password=hash_and_salted_password,
                key = request.form.get('key'),
                secret = request.form.get('secret'),

            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            print(current_user.name)
            return redirect(url_for("work"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('work'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/setup', methods=["GET", "POST"])
@login_required
def setup():
    if request.method == "POST":
        if request.form.getlist('classes') == []:
            return render_template("setup.html")
        else:
            values = request.form.getlist('classes')
            print(values)

            if check_if_duplicates(values):
                flash("Please remove duplicate class ids")
                # current_user.classes = str(values).replace("[", "").replace("]", "").replace("'", "").replace('"', '')
                db.session.commit()
                return redirect(url_for('setup'))
                # return render_template("setup.html")
            else:
                try:
                    # classes = str(values).replace("[", "").replace("]", "").replace("'", "").replace('"', '')
                    # print(classes)
                    get_assignments(key=current_user.key, secret=current_user.secret, classes=values)
                except requests.exceptions.HTTPError:
                    flash('invalid class ids')
                    return redirect(url_for("setup"))
                else:
                    current_user.classes = ",".join(values)
                    db.session.commit()
                    return redirect(url_for('work'))
    if current_user.classes is None:
        return render_template("setup.html", classes="NONE")
    else:
        return render_template("setup.html", classes=current_user.classes.split(","))



@app.route('/work')
@login_required
def work():
    time = datetime.datetime.now().strftime('%A %B %d, %Y')
    name = current_user.name
    if current_user.classes == None:
        return render_template("planner.html", time=time,  name=name, classes="NONE")
    else:
        # return render_template("setup.html", classes=(current_user.classes).split(","))
        assignments = get_assignments(key=current_user.key, secret=current_user.secret, classes=current_user.classes.split(","))
        return render_template("planner.html", time=time, assignments=assignments, name=name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Credit: https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
# @app.errorhandler(401)
# def error401(e):
#     # flash("401 error")
#     return render_template("unauthorized.html")

#     # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    # else:

# A decorator used to tell the application
# which URL is associated function





if __name__ == '__main__':
    app.run(debug=True)


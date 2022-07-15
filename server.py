from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import requests
import datetime
import schoolopy
import os



def get_assignments(key, secret, classes = None ):

    # Create a Schoology instance with Auth as a parameter.

    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))


    if classes == None:
        return "NONE"
    else:
        cl_list = []

        for i in classes:
            cl_list += (sc.get_assignments(i))
        return cl_list


app = Flask(__name__)

flask_key = os.urandom(12)

app.config['SECRET_KEY'] = flask_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

# Credit: https://thispointer.com/python-3-ways-to-check-if-there-are-duplicates-in-a-list/
def checkIfDuplicates(listOfElems):
    # ''' Check if given list contains any duplicates '''
    setOfElems = set()
    for elem in listOfElems:
        if elem in setOfElems:
            return True
        else:
            setOfElems.add(elem)
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
    global u_key, u_secret
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
        key = request.form.get('key')
        secret = request.form.get('secret')

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            global u_key, u_secret
            login_user(user)
            return redirect(url_for('work'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/setup', methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        if request.form.getlist('classes') == []:
            return render_template("setup.html")
        else:
            values = request.form.getlist('classes')
            if checkIfDuplicates(values) == True:
                flash("Please remove duplicate class ids")
                current_user.classes = str(values).replace("[", "").replace("]", "").replace("'", "").replace('"', '')
                db.session.commit()
                return redirect(url_for('setup'))
                # return render_template("setup.html")
            elif checkIfDuplicates(values) == False:
                current_user.classes = str(values).replace("[", "").replace("]", "").replace("'", "").replace('"', '')
                db.session.commit()
                return redirect(url_for('work'))
    if current_user.classes == None:
        return render_template("setup.html", classes="NONE")
    else:
        return render_template("setup.html", classes=(current_user.classes).split(","))



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

@app.errorhandler(401)
def not_logged_in(e):
    # note that we set the 404 status explicitly
    return render_template("unauthorized.html")

# A decorator used to tell the application
# which URL is associated function





if __name__ == '__main__':
    app.run(debug=True)


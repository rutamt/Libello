from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
import config
import main
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import requests
import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


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
            main.get_assignments(key=request.form.get('key'), secret=request.form.get('secret'))
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
                email=request.form.get('email'),
                name=request.form.get('name'),
                password=hash_and_salted_password,
                key = request.form.get('key'),
                secret = request.form.get('secret'),

            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
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

@app.route('/work')
@login_required
def work():
    time = datetime.datetime.now().strftime('%A %B %d, %Y')
    assignments = main.get_assignments(key= current_user.key, secret=current_user.secret)
    name=current_user.name
    return render_template("planner.html", time=time, assignments=assignments, name=name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# A decorator used to tell the application
# which URL is associated function





if __name__ == '__main__':
    app.run(debug=True)


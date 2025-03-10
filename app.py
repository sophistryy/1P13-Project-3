from flask import Flask, redirect, render_template, request
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from image_recognition.img_recognition import main
from models import db, User, SavedMusic
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "secret"

app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = "main_page"
login_manager.init_app(app)

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)

@app.route("/")
# "/" = home page; runs main at home page (in the broswer url, it's what comes after it)
# eg. 127.0.0.1:5000/ (this is main)

def main_page():
    a = [1, 3, "h", 4] # printing out an example list
    
    return render_template("base.html", a=a, test=True)
    # converts jinja page to html, passing variable into jinja (jinja just contains the python code within html
    # a=a is passing the variable into the html, while test=True is for the "Hello world !!" to show if test=True

@app.route("/2")
# this would be from 127.0.0.1:5000/2 instead of just the "/"
def secondpage():
    return render_template("display.html")

@app.route("/3")
def thirdpage():
    return render_template("index.html") 

@app.route("/get_json")
def get_json():
    # my_file = request.files["adasd"]
    # my_file.save("temp.png")

    # notes = main("temp.png")

    # saving data to user
    # notes = main("image") # json data
    # if current_user.is_authenticated:
    #     text_data = json.dumps(notes)
    #     music_obj = SavedMusic(user_id=current_user.id, data=text_data)
    #     db.session.add(music_obj)
    #     db.session.commit()

    image = "image_recognition\\ir_tests\\blues.jpg"

    return {
        "notes": main(image)
    }

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username").lower()
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()

    if user is not None:
        return render_template("register.html", error="That username is already taken")
    
    user = User(username=username, password=bcrypt.generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    login_user(user)

    return redirect("/")

@app.route("/logout")
def logout():
    logout_user()

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username").lower()
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()

    if user is None:
        return render_template("login.html", error="That username does not exist")
    
    if not bcrypt.check_password_hash(user.password, password):
        return render_template("login.html", error="Incorrect password")
    
    login_user(user)

    return redirect("/")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# just an ending thing 
if __name__ == "__main__":
    app.run(debug=True)

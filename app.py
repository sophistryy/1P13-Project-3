from flask import Flask, redirect, render_template, request
from flask_login import login_user, current_user, LoginManager, logout_user, login_required
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from image_recognition.img_recognition import main
from chord_reader.chord_reader import chord_reader

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
def base():
    if current_user.is_authenticated:
        return redirect("/library")

    return render_template("index.html")

@app.route("/display/<int:song_id>")
def display(song_id):
    song = SavedMusic.query.filter_by(id=song_id).first()

    if song is None:
        return redirect("/")
    
    return render_template("display.html", index=song_id, title=json.loads(song.data)["title"])

@app.route("/note_list/<int:song_id>")
def note_list(song_id):
    song = SavedMusic.query.filter_by(id=song_id).first()
    parsed_content = json.loads(song.data)

    if song is None:
        return redirect("/")
    
    return render_template("note_list.html", song=parsed_content, index=song_id)

@app.route("/library")
def library():
    songs = SavedMusic.query.filter_by(user_id=current_user.id).all()
    parsed_songs = {}

    for song in songs:
        parsed_songs[song.id] = json.loads(song.data)

    return render_template("library.html", songs=parsed_songs) 

@app.route("/get_song/<int:song_id>")
def get_song(song_id):
    song = SavedMusic.query.filter_by(id=song_id).first()

    if song is None:
        return {}
    
    return song.data

@app.route("/delete/<int:song_id>")
def delete_song(song_id):
    song = SavedMusic.query.filter_by(id=song_id).first()
    db.session.delete(song)
    db.session.commit()

    return redirect("/library")

@app.route("/set_name/<int:song_id>", methods=["POST"])
def set_name(song_id):
    song = SavedMusic.query.filter_by(id=song_id).first()
    song_data = json.loads(song.data)
    song_data["title"] = request.data.decode("utf-8")
    song.data = json.dumps(song_data)
    db.session.commit()
    return {}

@app.route("/get_json", methods=["POST"])
@login_required
def get_json():
    image = request.files.get("image")
    image.save("chord_reader\\temp.png")

    try:
        notes = main(image)
    except:
        try:
            notes = chord_reader("chord_reader\\temp.png")
        except Exception as e:
            return {
                "error": "Unable to read"
            }

    num_songs = len(SavedMusic.query.filter_by(user_id=current_user.id).all())
    text_data = {
        "notes": notes,
        "title": f"Song #{num_songs + 1}"
    }
    music_obj = SavedMusic(user_id=current_user.id, data=json.dumps(text_data))
    db.session.add(music_obj)
    db.session.commit()

    return {
        "id": music_obj.id
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

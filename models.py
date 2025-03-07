from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.Text, nullable=False)
    password = sa.Column(sa.Text, nullable=False)
    saved_music = db.relationship("SavedMusic", backref="user", lazy=True)

class SavedMusic(db.Model):
    __tablename__ = "saved_music"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    data = sa.Column(sa.Text, nullable=False)
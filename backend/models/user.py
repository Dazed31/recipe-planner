from sqlalchemy_serializer import SerializerMixin
from extensions import db


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-password_hash", "-settings.user", "-recipes.author")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user", nullable=False)  # "user" or "admin"

    settings = db.relationship("Settings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    recipes = db.relationship("Recipe", back_populates="author", cascade="all, delete-orphan")
from sqlalchemy_serializer import SerializerMixin
from extensions import db


class Settings(db.Model, SerializerMixin):
    __tablename__ = "settings"

    serialize_rules = ("-user.settings",)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    dietary_preference = db.Column(db.String, default="none")
    unit_system = db.Column(db.String, default="metric")

    user = db.relationship("User", back_populates="settings")
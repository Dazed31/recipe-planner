from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from extensions import db


class Recipe(db.Model, SerializerMixin):
    __tablename__ = "recipes"

    serialize_rules = ("-author.recipes", "-recipe_ingredients.recipe")

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)  # minutes

    author = db.relationship("User", back_populates="recipes")
    recipe_ingredients = db.relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")

    @validates("title")
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Recipe must have a title.")
        return value
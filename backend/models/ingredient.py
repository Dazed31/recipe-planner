from sqlalchemy_serializer import SerializerMixin
from extensions import db


class Ingredient(db.Model, SerializerMixin):
    __tablename__ = "ingredients"

    serialize_rules = ("-recipe_ingredients.ingredient", "-recipe_ingredients.recipe")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    recipe_ingredients = db.relationship("RecipeIngredient", back_populates="ingredient")
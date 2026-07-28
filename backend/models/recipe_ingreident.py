from sqlalchemy_serializer import SerializerMixin
from extensions import db


class RecipeIngredient(db.Model, SerializerMixin):
    __tablename__ = "recipe_ingredients"

    serialize_rules = ("-recipe.recipe_ingredients", "-ingredient.recipe_ingredients")

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)

    recipe = db.relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = db.relationship("Ingredient", back_populates="recipe_ingredients")
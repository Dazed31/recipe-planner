from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates 
from extensions import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ("-password_hash" , "-settings.user" , "recipes.author")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user", nullable=False) #user or admin

    settings = db.relationship('Settings', back_populates='user', uselist=False, cascade="all, delete-orphan")
    recipes = db.relationship('Recipe', back_populates='author', cascade="all, delete-orphan")


class Settings(db.Model, SerializerMixin):
    __tablename__ = 'settings'

    serialize_rules = ("-user.settings",)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dietary_preferences = db.Column(db.String, default="none")
    unit_systems = db.Column(db.String, default="metric")

    user = db.relationship('User', back_populates='settings')

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    serialize_rules = ("-author.recipes", "-recipe_ingredients.recipe")

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)  # in minutes

    author = db.relationship('User', back_populates='recipes')
    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade="all, delete-orphan")

    @validates("title")
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Recipe must have a title.")
        return value

class Ingredient(db.Model, SerializerMixin):
    __tablename__ = 'ingredients'

    serialize_rules = ("-recipe_ingredients.ingredient", "-ingredient.recipe_ingredients")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='ingredient')

class RecipeIngredient(db.Model, SerializerMixin):
    __tablename__ = 'recipe_ingredients'

    serialize_rules = ("-recipe.recipe_ingredients", "-ingredient.recipe_ingredients")

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)

    recipe = db.relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')

    

    
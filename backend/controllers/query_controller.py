from flask import request
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from extensions import db
from models import Recipe, Ingredient, RecipeIngredient, User


class RecipesByIngredientResource(Resource):
    """
    GET /recipes/search?ingredient=eggs
    Filters recipes across the many:many relationship to Ingredient.
    Demonstrates: join across relationship, .any() filter, eager loading.
    """
    def get(self):
        ingredient_name = request.args.get("ingredient")
        if not ingredient_name:
            return {"error": "ingredient query param is required"}, 400

        recipes = (
            Recipe.query
            .options(joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient))
            .filter(
                Recipe.recipe_ingredients.any(
                    RecipeIngredient.ingredient.has(
                        Ingredient.name.ilike(f"%{ingredient_name}%")
                    )
                )
            )
            .all()
        )

        return {
            "ingredient_searched": ingredient_name,
            "count": len(recipes),
            "recipes": [r.to_dict() for r in recipes],
        }, 200


class MostUsedIngredientsResource(Resource):
    """
    GET /ingredients/most-used
    Aggregates ingredient usage across all recipes.
    Demonstrates: join, func.count, group_by, order_by.
    """
    def get(self):
        limit = request.args.get("limit", 5, type=int)

        results = (
            db.session.query(
                Ingredient.id,
                Ingredient.name,
                func.count(RecipeIngredient.id).label("times_used"),
            )
            .join(RecipeIngredient, RecipeIngredient.ingredient_id == Ingredient.id)
            .group_by(Ingredient.id, Ingredient.name)
            .order_by(func.count(RecipeIngredient.id).desc())
            .limit(limit)
            .all()
        )

        return {
            "most_used_ingredients": [
                {"id": r.id, "name": r.name, "times_used": r.times_used}
                for r in results
            ]
        }, 200


class UserRecipeStatsResource(Resource):
    """
    GET /users/stats
    Aggregates recipe count and average prep time per user.
    Demonstrates: join, func.count, func.avg, group_by, having.
    """
    def get(self):
        min_recipes = request.args.get("min_recipes", 1, type=int)

        results = (
            db.session.query(
                User.id,
                User.username,
                func.count(Recipe.id).label("recipe_count"),
                func.avg(Recipe.prep_time).label("avg_prep_time"),
            )
            .join(Recipe, Recipe.user_id == User.id)
            .group_by(User.id, User.username)
            .having(func.count(Recipe.id) >= min_recipes)
            .order_by(func.count(Recipe.id).desc())
            .all()
        )

        return {
            "user_stats": [
                {
                    "user_id": r.id,
                    "username": r.username,
                    "recipe_count": r.recipe_count,
                    "avg_prep_time": round(float(r.avg_prep_time), 1) if r.avg_prep_time is not None else None,
                }
                for r in results
            ]
        }, 200
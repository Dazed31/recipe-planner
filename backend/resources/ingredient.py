from flask import request
from flask_restful import Resource
from extensions import db
from models import Ingredient
from resources.decorators import admin_required
from resources.recipe import paginated_response


class IngredientListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        query = Ingredient.query.order_by(Ingredient.name.asc())
        return paginated_response(query, page, per_page), 200

    @admin_required
    def post(self):
        data = request.get_json()
        name = data.get("name")
        if not name:
            return {"error": "name is required"}, 400
        if Ingredient.query.filter_by(name=name).first():
            return {"error": "ingredient already exists"}, 409

        ingredient = Ingredient(name=name)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient.to_dict(), 201


class IngredientResource(Resource):
    def get(self, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return {"error": "ingredient not found"}, 404
        return ingredient.to_dict(), 200

    @admin_required
    def patch(self, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return {"error": "ingredient not found"}, 404

        data = request.get_json()
        if "name" in data:
            ingredient.name = data["name"]
        db.session.commit()
        return ingredient.to_dict(), 200

    @admin_required
    def delete(self, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return {"error": "ingredient not found"}, 404

        db.session.delete(ingredient)
        db.session.commit()
        return {}, 204
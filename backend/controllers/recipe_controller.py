from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models import Recipe, RecipeIngredient, Ingredient


def paginated_response(query, page, per_page):
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": [item.to_dict() for item in paginated.items],
        "total": paginated.total,
        "page": paginated.page,
        "per_page": paginated.per_page,
        "total_pages": paginated.pages,
    }


class RecipeListResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        query = Recipe.query.order_by(Recipe.id.desc())
        return paginated_response(query, page, per_page), 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()

        title = data.get("title")
        instructions = data.get("instructions")
        prep_time = data.get("prep_time")
        ingredients = data.get("ingredients", [])  # [{ingredient_id, quantity, unit}, ...]

        if not title or not instructions:
            return {"error": "title and instructions are required"}, 400

        try:
            recipe = Recipe(
                user_id=int(user_id),
                title=title,
                instructions=instructions,
                prep_time=prep_time,
            )
            db.session.add(recipe)
            db.session.flush()

            for item in ingredients:
                ingredient_id = item.get("ingredient_id")
                quantity = item.get("quantity")
                unit = item.get("unit")
                if not Ingredient.query.get(ingredient_id):
                    db.session.rollback()
                    return {"error": f"ingredient_id {ingredient_id} does not exist"}, 400
                db.session.add(RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient_id,
                    quantity=quantity,
                    unit=unit,
                ))

            db.session.commit()
            return recipe.to_dict(), 201

        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class RecipeResource(Resource):
    def get(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {"error": "recipe not found"}, 404
        return recipe.to_dict(), 200

    @jwt_required()
    def patch(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {"error": "recipe not found"}, 404

        user_id = get_jwt_identity()
        role = get_jwt().get("role")
        if str(recipe.user_id) != str(user_id) and role != "admin":
            return {"error": "you can only edit your own recipes"}, 403

        data = request.get_json()
        try:
            if "title" in data:
                recipe.title = data["title"]
            if "instructions" in data:
                recipe.instructions = data["instructions"]
            if "prep_time" in data:
                recipe.prep_time = data["prep_time"]
            db.session.commit()
            return recipe.to_dict(), 200
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {"error": "recipe not found"}, 404

        user_id = get_jwt_identity()
        role = get_jwt().get("role")
        if str(recipe.user_id) != str(user_id) and role != "admin":
            return {"error": "you can only delete your own recipes"}, 403

        db.session.delete(recipe)
        db.session.commit()
        return {}, 204
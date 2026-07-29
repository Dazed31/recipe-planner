from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt, api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    from models import User, Settings, Recipe, Ingredient, RecipeIngredient  # noqa: F401
    from controllers.auth_controller import (
        RegisterResource,
        LoginResource,
        MeResource,
        AdminPingResource,
    )
    from controllers.recipe_controller import RecipeListResource, RecipeResource
    from controllers.ingredient_controller import IngredientListResource, IngredientResource
    from controllers.query_controller import (
        RecipesByIngredientResource,
        MostUsedIngredientsResource,
        UserRecipeStatsResource,
    )

    api.add_resource(RegisterResource, "/register")
    api.add_resource(LoginResource, "/login")
    api.add_resource(MeResource, "/me")
    api.add_resource(AdminPingResource, "/admin/ping")
    api.add_resource(RecipeListResource, "/recipes")
    api.add_resource(RecipeResource, "/recipes/<int:recipe_id>")
    api.add_resource(IngredientListResource, "/ingredients")
    api.add_resource(IngredientResource, "/ingredients/<int:ingredient_id>")
    api.add_resource(RecipesByIngredientResource, "/recipes/search")
    api.add_resource(MostUsedIngredientsResource, "/ingredients/most-used")
    api.add_resource(UserRecipeStatsResource, "/users/stats")
    api.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

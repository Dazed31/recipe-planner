from faker import Faker
from werkzeug.security import generate_password_hash
from main import create_app
from extensions import db
from models import User, Settings, Recipe, Ingredient, RecipeIngredient

fake = Faker()
app = create_app()

INGREDIENT_NAMES = [
    "Flour", "Sugar", "Eggs", "Butter", "Milk", "Salt", "Black Pepper",
    "Olive Oil", "Garlic", "Onion", "Chicken", "Ground Beef", "Bacon",
    "Spaghetti", "Arborio Rice", "Parmesan", "Feta", "Cheddar Cheese",
    "Tomato", "Cherry Tomatoes", "Basil", "Lettuce", "Cucumber",
    "Bell Pepper", "Mushroom", "Banana", "Chocolate Chips",
    "Vanilla Extract", "Baking Powder", "Soy Sauce", "Lemon",
    "Taco Shells", "Vegetable Broth",
]

RECIPES = [
    {
        "title": "Classic Spaghetti Carbonara",
        "prep_time": 25,
        "instructions": "Cook spaghetti in salted boiling water until al dente. Meanwhile, fry the bacon until crisp. Whisk eggs with grated parmesan and black pepper in a bowl. Drain the pasta, reserving a splash of pasta water, then toss immediately with the bacon and egg mixture off the heat, adding pasta water until glossy and creamy. Serve right away with extra parmesan.",
        "ingredients": [
            ("Spaghetti", 200, "g"),
            ("Bacon", 100, "g"),
            ("Eggs", 2, "whole"),
            ("Parmesan", 50, "g"),
            ("Black Pepper", 1, "tsp"),
        ],
    },
    {
        "title": "Fluffy Buttermilk Pancakes",
        "prep_time": 20,
        "instructions": "Whisk flour, sugar, and baking powder together. In a separate bowl, whisk milk, eggs, and melted butter. Combine wet and dry ingredients until just mixed, a few lumps are fine. Cook spoonfuls on a hot buttered griddle until bubbles form on top, then flip and cook until golden.",
        "ingredients": [
            ("Flour", 1.5, "cup"),
            ("Milk", 1.25, "cup"),
            ("Eggs", 2, "whole"),
            ("Sugar", 2, "tbsp"),
            ("Baking Powder", 1, "tbsp"),
            ("Butter", 2, "tbsp"),
        ],
    },
    {
        "title": "Garlic Butter Chicken",
        "prep_time": 30,
        "instructions": "Season chicken with salt and pepper. Sear in olive oil until golden on both sides. Lower the heat, add butter and crushed garlic, and baste the chicken in the foaming garlic butter for a few minutes until cooked through. Rest briefly before serving.",
        "ingredients": [
            ("Chicken", 500, "g"),
            ("Butter", 3, "tbsp"),
            ("Garlic", 4, "whole"),
            ("Olive Oil", 1, "tbsp"),
            ("Salt", 1, "tsp"),
            ("Black Pepper", 1, "tsp"),
        ],
    },
    {
        "title": "Vegetable Stir Fry",
        "prep_time": 20,
        "instructions": "Heat olive oil in a wok over high heat. Add garlic and onion, stir-fry until fragrant. Add bell pepper and mushroom, stir-fry until just tender. Splash in soy sauce, toss to coat, and serve immediately over rice.",
        "ingredients": [
            ("Bell Pepper", 1, "whole"),
            ("Onion", 1, "whole"),
            ("Mushroom", 150, "g"),
            ("Soy Sauce", 3, "tbsp"),
            ("Olive Oil", 2, "tbsp"),
            ("Garlic", 2, "whole"),
        ],
    },
    {
        "title": "Banana Bread",
        "prep_time": 65,
        "instructions": "Mash the bananas and mix with melted butter, sugar, and eggs. Fold in flour and baking powder until just combined. Pour into a greased loaf pan and bake at 175°C for about 50 minutes, until a skewer comes out clean.",
        "ingredients": [
            ("Banana", 3, "whole"),
            ("Flour", 2, "cup"),
            ("Sugar", 0.75, "cup"),
            ("Butter", 0.5, "cup"),
            ("Eggs", 2, "whole"),
            ("Baking Powder", 1, "tsp"),
        ],
    },
    {
        "title": "Greek Salad",
        "prep_time": 15,
        "instructions": "Chop cucumber, tomatoes, and onion. Combine in a bowl with crumbled feta. Dress with olive oil and a squeeze of lemon, season with salt, and toss gently.",
        "ingredients": [
            ("Cucumber", 1, "whole"),
            ("Cherry Tomatoes", 200, "g"),
            ("Feta", 100, "g"),
            ("Olive Oil", 3, "tbsp"),
            ("Lemon", 1, "whole"),
            ("Onion", 0.5, "whole"),
        ],
    },
    {
        "title": "Tomato Basil Soup",
        "prep_time": 35,
        "instructions": "Sauté onion and garlic in olive oil until soft. Add chopped tomatoes and vegetable broth, simmer for 20 minutes. Blend until smooth, stir through torn basil, and season to taste.",
        "ingredients": [
            ("Tomato", 800, "g"),
            ("Onion", 1, "whole"),
            ("Garlic", 3, "whole"),
            ("Vegetable Broth", 500, "ml"),
            ("Basil", 10, "g"),
            ("Olive Oil", 2, "tbsp"),
        ],
    },
    {
        "title": "Beef Tacos",
        "prep_time": 25,
        "instructions": "Brown the ground beef with chopped onion. Warm the taco shells. Fill each shell with beef, shredded lettuce, diced tomato, and grated cheddar. Serve with lime on the side.",
        "ingredients": [
            ("Ground Beef", 400, "g"),
            ("Taco Shells", 8, "whole"),
            ("Cheddar Cheese", 100, "g"),
            ("Lettuce", 100, "g"),
            ("Tomato", 2, "whole"),
            ("Onion", 0.5, "whole"),
        ],
    },
    {
        "title": "Chocolate Chip Cookies",
        "prep_time": 30,
        "instructions": "Cream butter and sugar until light. Beat in eggs and vanilla. Fold in flour, then stir through chocolate chips. Scoop onto a lined tray and bake at 180°C for 10-12 minutes until golden at the edges.",
        "ingredients": [
            ("Flour", 2.25, "cup"),
            ("Butter", 1, "cup"),
            ("Sugar", 0.75, "cup"),
            ("Chocolate Chips", 2, "cup"),
            ("Eggs", 2, "whole"),
            ("Vanilla Extract", 1, "tsp"),
        ],
    },
    {
        "title": "Creamy Mushroom Risotto",
        "prep_time": 40,
        "instructions": "Sauté onion in butter until translucent. Add arborio rice and toast briefly. Add warm vegetable broth one ladle at a time, stirring constantly, until the rice is creamy and just tender. Stir through sautéed mushrooms and parmesan before serving.",
        "ingredients": [
            ("Arborio Rice", 1.5, "cup"),
            ("Mushroom", 250, "g"),
            ("Vegetable Broth", 1, "l"),
            ("Parmesan", 60, "g"),
            ("Onion", 1, "whole"),
            ("Butter", 2, "tbsp"),
        ],
    },
]

with app.app_context():
    print("Clearing tables...")
    RecipeIngredient.query.delete()
    Recipe.query.delete()
    Ingredient.query.delete()
    Settings.query.delete()
    User.query.delete()

    print("Seeding users...")
    admin = User(
        username="admin",
        email="admin@example.com",
        password_hash=generate_password_hash("admin123"),
        role="admin",
    )
    admin.settings = Settings(dietary_preference="none", unit_system="metric")
    db.session.add(admin)

    users = []
    for _ in range(5):
        u = User(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password_hash=generate_password_hash("password123"),
            role="user",
        )
        u.settings = Settings(
            dietary_preference=fake.random_element(["none", "vegetarian", "vegan", "gluten-free"]),
            unit_system=fake.random_element(["metric", "imperial"]),
        )
        users.append(u)
        db.session.add(u)

    db.session.commit()

    print("Seeding ingredients...")
    ingredients_by_name = {}
    for name in INGREDIENT_NAMES:
        ing = Ingredient(name=name)
        db.session.add(ing)
        ingredients_by_name[name] = ing
    db.session.commit()

    print("Seeding recipes + recipe_ingredients...")
    all_authors = [admin] + users
    for i, recipe_data in enumerate(RECIPES):
        recipe = Recipe(
            author=all_authors[i % len(all_authors)],
            title=recipe_data["title"],
            instructions=recipe_data["instructions"],
            prep_time=recipe_data["prep_time"],
        )
        db.session.add(recipe)
        db.session.flush()

        for ing_name, quantity, unit in recipe_data["ingredients"]:
            db.session.add(RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredients_by_name[ing_name].id,
                quantity=quantity,
                unit=unit,
            ))

    db.session.commit()
    print("Done seeding.")
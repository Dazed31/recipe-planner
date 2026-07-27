from faker import Faker
from werkzeug.security import generate_password_hash
from app import create_app
from extensions import db
from models import User, Settings, Recipe, Ingredient, RecipeIngredient

fake = Faker()
app = create_app()

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
    ingredient_names = ["Flour", "Sugar", "Eggs", "Butter", "Milk", "Salt", "Olive Oil", "Garlic", "Onion", "Chicken"]
    ingredients = [Ingredient(name=n) for n in ingredient_names]
    db.session.add_all(ingredients)
    db.session.commit()

    print("Seeding recipes + recipe_ingredients...")
    for _ in range(15):
        recipe = Recipe(
            author=fake.random_element(users),
            title=fake.sentence(nb_words=3).rstrip("."),
            instructions=fake.paragraph(nb_sentences=5),
            prep_time=fake.random_int(min=10, max=90),
        )
        db.session.add(recipe)
        db.session.flush()

        for ingredient in fake.random_elements(ingredients, length=fake.random_int(min=3, max=6), unique=True):
            db.session.add(RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=round(fake.random.uniform(0.5, 3), 2),
                unit=fake.random_element(["g", "kg", "ml", "l", "tsp", "tbsp", "cup"]),
            ))

    db.session.commit()
    print("Done seeding.")
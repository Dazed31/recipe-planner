from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt, api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    # Enable CORS
    CORS(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
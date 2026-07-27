from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db
from models import User, Settings


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"error": "username, email, and password are required"}, 400

        if User.query.filter_by(username=username).first():
            return {"error": "username already taken"}, 409
        if User.query.filter_by(email=email).first():
            return {"error": "email already registered"}, 409

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role="user",
        )
        user.settings = Settings()
        db.session.add(user)
        db.session.commit()

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role},
        )
        return {"token": token, "user": user.to_dict()}, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {"error": "invalid username or password"}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role},
        )
        return {"token": token, "user": user.to_dict()}, 200
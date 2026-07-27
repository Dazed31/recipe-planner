from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models import User, Settings
from resources.decorators import admin_required


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


class MeResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return {"user_id": user_id, "role": get_jwt().get("role")}, 200


class AdminPingResource(Resource):
    @admin_required
    def get(self):
        return {"message": "you are an admin, congrats"}, 200
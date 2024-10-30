from flask import Flask, jsonify

from backend import app, db
from backend.models.user import User
from backend.services.user_service import delete_user, login, signup
from backend.utils import token_required


# Rota para criar um novo usuário
@app.route("/users", methods=["POST"])
def signup_route():
    response, status_code = signup()
    return jsonify(response), status_code


# Rota para fazer login
@app.route("/login", methods=["POST"])
def login_route():
    response, status_code = login()
    return jsonify(response), status_code


# Rota para deletar um usuário e todos os seus personagens
@app.route("/users/<hashed_id>", methods=["DELETE"])
@token_required
def delete_user_route(current_user, hashed_id):
    response, status_code = delete_user(current_user, hashed_id)
    return jsonify(response), status_code

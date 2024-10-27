
from flask import Flask, jsonify

from backend.utils import token_required

from backend import app, db
from backend.models.user import User
from backend.services.user_service import login, signup, delete_user


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
@app.route("/users/<int:id>", methods=["DELETE"])
@token_required
def delete_user_route(current_user, id):
    response, status_code = delete_user(current_user, id)
    return jsonify(response), status_code
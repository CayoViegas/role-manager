from flask import Flask, jsonify

from backend.utils import token_required

from backend import app
from backend.models.character import Character
from backend.services.character_service import create_character, get_characters, get_character, update_character, delete_character


# Rota para criar um novo personagem (agora vinculado ao usuário)
@app.route("/characters", methods=["POST"])
@token_required
def create_character_route(current_user):
    response, status = create_character(current_user)
    return jsonify(response), status


# Rota para listar todos os personagens do usuário logado
@app.route("/characters", methods=["GET"])
@token_required
def get_characters_route(current_user):
    response, status = get_characters(current_user)
    return jsonify(response), status


# Rota para buscar um personagem específico do usuário logado por ID
@app.route("/characters/<int:id>", methods=["GET"])
@token_required
def get_character_route(current_user, id):
    response, status = get_character(current_user, id)
    return jsonify(response), status


# Rota para editar um personagem existente
@app.route("/characters/<int:id>", methods=["PUT"])
@token_required
def update_character_route(current_user, id):
    response, status = update_character(current_user, id)
    return jsonify(response), status


# Rota para deletar um personagem do usuário
@app.route("/characters/<int:id>", methods=["DELETE"])
@token_required
def delete_character_route(current_user, id):
    response, status = delete_character(current_user, id)
    return jsonify(response), status
    
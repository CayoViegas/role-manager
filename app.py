from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from . import app
from .models import Character, User, db


# Rota para criar um novo usuário
@app.route("/users", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user:
            return (
                jsonify({"message": "Usuário já existe. Por favor, faça login."}),
                200,
            )
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "username": user.username}), 201
    return jsonify({"message": "Usuário ou senha inválidos."}), 400


# Rota para criar um novo personagem
@app.route("/characters", methods=["POST"])
def create_character():
    data = request.get_json()
    new_character = Character(
        name=data["name"], race=data["race"], class_=data["class_"], level=data["level"]
    )
    db.session.add(new_character)
    db.session.commit()
    return (
        jsonify(
            {
                "id": new_character.id,
                "name": new_character.name,
                "race": new_character.race,
                "class": new_character.class_,
                "level": new_character.level,
            }
        ),
        201,
    )


# Rota para listar todos os personagens
@app.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    return (
        jsonify(
            [
                {
                    "id": character.id,
                    "name": character.name,
                    "race": character.race,
                    "class": character.class_,
                    "level": character.level,
                }
                for character in characters
            ]
        ),
        200,
    )


# Rota para buscar um personagem específico por ID
@app.route("/characters/<int:id>", methods=["GET"])
def get_character(id):
    character = Character.query.get_or_404(id)
    return (
        jsonify(
            {
                "id": character.id,
                "name": character.name,
                "race": character.race,
                "class": character.class_,
                "level": character.level,
            }
        ),
        200,
    )


# Rota para editar um personagem existente
@app.route("/characters/<int:id>", methods=["PUT"])
def update_character(id):
    character = Character.query.get_or_404(id)
    data = request.get_json()

    character.name = data.get("name", character.name)
    character.race = data.get("race", character.race)
    character.class_ = data.get("class_", character.class_)
    character.level = data.get("level", character.level)

    db.session.commit()
    return (
        jsonify(
            {
                "id": character.id,
                "name": character.name,
                "race": character.race,
                "class": character.class_,
                "level": character.level,
            }
        ),
        200,
    )


# Rota para deletar um personagem
@app.route("/characters/<int:id>", methods=["DELETE"])
def delete_character(id):
    character = Character.query.get_or_404(id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Personagem deletado com sucesso."}), 200

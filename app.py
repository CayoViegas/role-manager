from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from . import app
from .models import Character, User, db


# Configuração para retornar JSON com UTF-8
@app.after_request
def after_request(response):
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


# Função de verificação de token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]  # O token está no formato "Bearer <token>"
        if not token:
            return jsonify({"message": "Token não encontrado."}), 401

        try:
            data = jwt.decode(token, "how-to-find-true-love-and-happiness", algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["id"]).first()
        except Exception as e:
            print(e)
            return jsonify({"message": "Token inválido."}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# Rota para criar um novo usuário
@app.route("/users", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    is_superuser = data.get("is_superuser", False)  # O campo is_superuser é opcional e tem False como valor padrão

    if not isinstance(username, str) or len(username) < 3 or len(username) > 50:
        return jsonify({"message": "Nome de usuário inválido. Deve conter entre 3 e 50 caracteres."}), 400
    if not isinstance(password, str) or len(password) < 6 or len(password) > 12:
        return jsonify({"message": "Senha inválida. Deve conter entre 6 e 12 caracteres."}), 400

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user:
            return (
                jsonify({"message": "Usuário já existe. Por favor, faça login."}),
                200,
            )
        user = User(username=username, password=generate_password_hash(password), is_superuser=is_superuser)
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "username": user.username, "is_superuser": user.is_superuser}), 201
    return jsonify({"message": "Usuário ou senha inválidos."}), 400


# Rota para fazer login
@app.route("/login", methods=["POST"])
def login():
    auth = request.json

    if not auth or not auth.get("username") or not auth.get("password"):
        return (
            jsonify({"message": "Usuário ou senha inválidos."}),
            401,
        )

    user = User.query.filter_by(username=auth.get("username")).first()

    if not user:
        return (
            jsonify({"message": "Usuário ou senha inválidos."}),
            401,
        )
    if check_password_hash(user.password, auth.get("password")):
        token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
            },
            "how-to-find-true-love-and-happiness",
            "HS256",
        )
        return jsonify({"token": token}, 201)
    return jsonify({"message": "Usuário ou senha inválidos."}), 401


# Rota para criar um novo personagem (agora vinculado ao usuário)
@app.route("/characters", methods=["POST"])
@token_required
def create_character(current_user):
    data = request.get_json()

    # Validação dos campos
    name = data.get("name")
    race = data.get("race")
    class_ = data.get("class_")
    level = data.get("level", 1)  # O nível é opcional e tem 1 como valor padrão

    if not isinstance(name, str) or len(name) < 1 or len(name) > 128:
        return jsonify({"message": "Nome inválido. Deve conter entre 1 e 128 caracteres."}), 400
    if not isinstance(race, str) or len(race) < 1 or len(race) > 128:
        return jsonify({"message": "Raça inválida. Deve conter entre 1 e 128 caracteres."}), 400
    if not isinstance(class_, str) or len(class_) < 1 or len(class_) > 128:
        return jsonify({"message": "Classe inválida. Deve conter entre 1 e 128 caracteres."}), 400
    if not isinstance(level, int) or level < 1:
        return jsonify({"message": "Nível inválido. Deve ser um número inteiro positivo."}), 400

    new_character = Character(
        name=name,
        race=race,
        class_=class_,
        level=level,
        user_id=current_user.id,
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
                "user_id": new_character.user_id,
            }
        ),
        201,
    )


# Rota para listar todos os personagens do usuário logado
@app.route("/characters", methods=["GET"])
@token_required
def get_characters(current_user):

    if current_user.is_superuser:
        characters = Character.query.all()
    else:
        characters = current_user.characters

    if not characters:
        return jsonify({"message": "Nenhum personagem encontrado."}), 404

    return (
        jsonify(
            [
                {
                    "id": character.id,
                    "name": character.name,
                    "race": character.race,
                    "class": character.class_,
                    "level": character.level,
                    "user_id": character.user_id,
                }
                for character in characters
            ]
        ),
        200,
    )


# Rota para buscar um personagem específico do usuário logado por ID
@app.route("/characters/<int:id>", methods=["GET"])
@token_required
def get_character(current_user, id):

    if current_user.is_superuser:
        character = Character.query.filter_by(id=id).first()
    else:
        character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return jsonify({"message": "Personagem não encontrado."}), 404

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
@token_required
def update_character(current_user, id):
    character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return jsonify({"message": "Personagem não encontrado."}), 404

    data = request.get_json()

    # Validação dos campos
    name = data.get("name", character.name)
    race = data.get("race", character.race)
    class_ = data.get("class_", character.class_)
    level = data.get("level", character.level)

    if not isinstance(name, str) or len(name) < 1 or len(name) > 128:
        return jsonify({"message": "Nome inválido. Deve conter entre 1 e 128 caracteres."}), 400
    if not isinstance(race, str) or len(race) < 1 or len(race) > 128:
        return jsonify({"message": "Raça inválida. Deve conter entre 1 e 128 caracteres."}), 400
    if not isinstance(class_, str) or len(class_) < 1 or len(class_) > 128:
        return jsonify({"message": "Classe inválida. Deve conter entre 1 e 128 caracteres."}), 400
    if not isinstance(level, int) or level < 1:
        return jsonify({"message": "Nível inválido. Deve ser um número inteiro positivo."}), 400

    character.name = name
    character.race = race
    character.class_ = class_
    character.level = level

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


# Rota para deletar um personagem do usuário
@app.route("/characters/<int:id>", methods=["DELETE"])
@token_required
def delete_character(current_user, id):

    if current_user.is_superuser:
        character = Character.query.filter_by(id=id).first()
    else:
        character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return jsonify({"message": "Personagem não encontrado."}), 404

    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Personagem deletado com sucesso."}), 200


# Rota para deletar um usuário e todos os seus personagens
@app.route("/users/<int:id>", methods=["DELETE"])
@token_required
def delete_user(current_user, id):
    if current_user.id != id:
        return jsonify({"message": "Você só pode deletar sua própria conta."}), 403

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({"message": "Usuário não encontrado."}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuário e seus personagens foram deletados com sucesso."}), 200

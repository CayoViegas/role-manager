from flask import Flask, request, jsonify
from .models import Character, db
from . import app

# Rota para criar um novo personagem
@app.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    new_character = Character(
        name=data['name'],
        race=data['race'],
        class_=data['class_'],
        level=data['level']
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({
        'id': new_character.id,
        'name': new_character.name,
        'race': new_character.race,
        'class': new_character.class_,
        'level': new_character.level
    }), 201

# Rota para listar todos os personagens
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([{
        'id': character.id,
        'name': character.name,
        'race': character.race,
        'class': character.class_,
        'level': character.level
    } for character in characters]), 200

# Rota para buscar um personagem específico por ID
@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get_or_404(id)
    return jsonify({
        'id': character.id,
        'name': character.name,
        'race': character.race,
        'class': character.class_,
        'level': character.level
    }), 200

# Rota para editar um personagem existente
@app.route('/characters/<int:id>', methods=['PUT'])
def update_character(id):
    character = Character.query.get_or_404(id)
    data = request.get_json()

    character.name = data.get('name', character.name)
    character.race = data.get('race', character.race)
    character.class_ = data.get('class_', character.class_)
    character.level = data.get('level', character.level)

    db.session.commit()
    return jsonify({
        'id': character.id,
        'name': character.name,
        'race': character.race,
        'class': character.class_,
        'level': character.level
    }), 200

# Rota para deletar um personagem
@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get_or_404(id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Personagem deletado com sucesso."}), 200
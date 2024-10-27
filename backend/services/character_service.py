from flask import request

from backend.models.character import Character
from backend import db

def create_character(current_user):
    data = request.get_json()

    # Validação dos campos
    name = data.get("name")
    race = data.get("race")
    class_ = data.get("class_")
    level = data.get("level", 1)  # O nível é opcional e tem 1 como valor padrão

    if not isinstance(name, str) or len(name) < 1 or len(name) > 128:
        return {"message": "Nome inválido. Deve conter entre 1 e 128 caracteres."}, 400
    if not isinstance(race, str) or len(race) < 1 or len(race) > 128:
        return {"message": "Raça inválida. Deve conter entre 1 e 128 caracteres."}, 400
    if not isinstance(class_, str) or len(class_) < 1 or len(class_) > 128:
        return {"message": "Classe inválida. Deve conter entre 1 e 128 caracteres."}, 400
    if not isinstance(level, int) or level < 1:
        return {"message": "Nível inválido. Deve ser um número inteiro positivo."}, 400

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
            {
                "id": new_character.id,
                "name": new_character.name,
                "race": new_character.race,
                "class": new_character.class_,
                "level": new_character.level,
                "user_id": new_character.user_id,
            }
        ,
        201,
    )

def get_characters(current_user):
    if current_user.is_superuser:
        characters = Character.query.all()
    else:
        characters = current_user.characters

    if not characters:
        return {"message": "Nenhum personagem encontrado."}, 404

    return (
            [
                {
                    "id": character.id,
                    "name": character.name,
                    "race": character.race,
                    "class": character.class_,
                    "level": character.level,
                    "user_id": character.user_id,
                    "owner": character.user.username if current_user.is_superuser else None,
                }
                for character in characters
            ]
        ,
        200,
    )
    
def get_character(current_user, id):
    if current_user.is_superuser:
        character = Character.query.filter_by(id=id).first()
    else:
        character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return {"message": "Personagem não encontrado."}, 404

    return (
            {
                "id": character.id,
                "name": character.name,
                "race": character.race,
                "class": character.class_,
                "level": character.level,
            }
        ,
        200,
    )

def update_character(current_user, id):
    character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return {"message": "Personagem não encontrado."}, 404

    data = request.get_json()

    # Validação dos campos
    name = data.get("name", character.name)
    race = data.get("race", character.race)
    class_ = data.get("class_", character.class_)
    level = data.get("level", character.level)

    if not isinstance(name, str) or len(name) < 1 or len(name) > 128:
        return {"message": "Nome inválido. Deve conter entre 1 e 128 caracteres."}, 400
    if not isinstance(race, str) or len(race) < 1 or len(race) > 128:
        return {"message": "Raça inválida. Deve conter entre 1 e 128 caracteres."}, 400
    if not isinstance(class_, str) or len(class_) < 1 or len(class_) > 128:
        return {"message": "Classe inválida. Deve conter entre 1 e 128 caracteres."}, 400
    if not isinstance(level, int) or level < 1:
        return {"message": "Nível inválido. Deve ser um número inteiro positivo."}, 400

    character.name = name
    character.race = race
    character.class_ = class_
    character.level = level

    db.session.commit()
    return (
            {
                "id": character.id,
                "name": character.name,
                "race": character.race,
                "class": character.class_,
                "level": character.level,
            }
        ,
        200,
    )

def delete_character(current_user, id):
    if current_user.is_superuser:
        character = Character.query.filter_by(id=id).first()
    else:
        character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return {"message": "Personagem não encontrado."}, 404

    db.session.delete(character)
    db.session.commit()
    return {"message": "Personagem deletado com sucesso."}, 200
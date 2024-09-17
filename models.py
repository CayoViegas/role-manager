from . import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False) # Campo para definir se o usuário é um superusuário

    # Relacionamento um-para-muitos: um usuário pode ter vários personagem. Exclusão em cascata
    characters = db.relationship("Character", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # Chave estrangeira para o usuário
    name = db.Column(db.String(128), nullable=False, unique=True)
    race = db.Column(db.String(128), nullable=False)
    class_ = db.Column(db.String(128), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Character {self.name}>"

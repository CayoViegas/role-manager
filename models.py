from . import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    character = db.relationship("characters", backref="users")

    def __repr__(self):
        return f"<User {self.username}>"


class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    class_ = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Character {self.name}>"

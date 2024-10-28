from backend import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)  # Campo para definir se o usuário é um superusuário

    # Relacionamento um-para-muitos: um usuário pode ter vários personagem. Exclusão em cascata
    characters = db.relationship("Character", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

from backend import db

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
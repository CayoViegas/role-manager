from . import db

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    class_ = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Character {self.name}>"
from flask import Flask, json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost:5432/role-manager"
json.provider.DefaultJSONProvider.ensure_ascii = False


db.init_app(app)
CORS(app)


from backend.routes import character_routes, user_routes

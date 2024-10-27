from functools import wraps

from flask import jsonify, request
import jwt
from backend.models.user import User


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
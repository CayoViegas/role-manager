import hmac
import hashlib
import base64

from functools import wraps

import jwt
from flask import jsonify, request

from backend.models.user import User


SECRET_KEY = "vinicius-41kg-de-massa-magra"

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


def hash_user_id(user_id):
    """Gera um hash único e reversível para o ID do usuário."""
    # Usar HMAC com SHA256 para hash do ID
    hmac_hash = hmac.new(SECRET_KEY.encode(), str(user_id).encode(), hashlib.sha256).digest()
    # Codificar hash em base64
    encoded_id = base64.urlsafe_b64encode(hmac_hash).decode()
    return encoded_id

def decode_hashed_id(hashed_id):
    """Recupera o ID original a partir do hash."""
    for user in User.query.all():
        if hash_user_id(user.id) == hashed_id:
            return user.id
        
    return None
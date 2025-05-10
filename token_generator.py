import jwt
import datetime
from models import db, Orders, Customers


class TokenGenerator:
    SECRET_KEY = "your_secret_key"

    @staticmethod
    def generate_token(user_id, role_type):
        payload = {
            "user_id": user_id,
            "role_type": role_type,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, TokenGenerator.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, TokenGenerator.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    @staticmethod
    def is_authorized(token, required_role):
        try:
            decoded = TokenGenerator.decode_token(token)
            if decoded["role_type"] != required_role:
                raise ValueError("Unauthorized access")
            return True
        except ValueError as e:
            raise ValueError(str(e))

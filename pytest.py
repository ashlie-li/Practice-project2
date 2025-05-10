import pytest
import jwt
import datetime
from token_generator import TokenGenerator

# filepath: /Users/nili/Documents/Git/Toy_projects/Practice-project2/test_token_generator.py


def test_decode_valid_token():
    # Arrange
    user_id = 1
    role_type = "admin"
    token = TokenGenerator.generate_token(user_id, role_type)

    # Act
    decoded = TokenGenerator.decode_token(token)

    # Assert
    assert decoded["user_id"] == user_id
    assert decoded["role_type"] == role_type


def test_decode_expired_token():
    # Arrange
    expired_payload = {
        "user_id": 1,
        "role_type": "admin",
        "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
    }
    expired_token = jwt.encode(
        expired_payload, TokenGenerator.SECRET_KEY, algorithm="HS256")

    # Act & Assert
    with pytest.raises(ValueError, match="Token has expired"):
        TokenGenerator.decode_token(expired_token)


def test_decode_invalid_token():
    # Arrange
    invalid_token = "invalid.token.string"

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid token"):
        TokenGenerator.decode_token(invalid_token)

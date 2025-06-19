import jwt
import datetime

JWT_SECRET = "your-super-secret-key"
ALGORITHM = "HS256"


def create_token(user_id: str = "test_user", role: str = "admin") -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token


if __name__ == "__main__":
    token = create_token()
    print(f"Your test JWT token:\n\nBearer {token}\n")

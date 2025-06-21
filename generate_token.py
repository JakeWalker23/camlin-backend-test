import jwt
import datetime

from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

def create_token(user_id: str = "test_user", role: str = "admin") -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


if __name__ == "__main__":
    token = create_token()
    print(f"Your test JWT token:\n\nBearer {token}\n")

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends
import jwt

from dotenv import load_dotenv
import os

load_dotenv()

class AuthService:

    @staticmethod
    async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        JWT_SECRET = os.getenv('JWT_SECRET')
        JWT_ALGORITHM = os.getenv('JWT_ALGORITHM') 

        token = credentials.credentials
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        
        if payload.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User Unauthorised",
            )
        
        return payload

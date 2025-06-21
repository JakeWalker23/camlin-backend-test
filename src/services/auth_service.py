from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends
import jwt

class AuthService:
    def __init__(self, secret: str = "your-super-secret-key", algorithm: str = "HS256"):
        self.JWT_SECRET = secret
        self.ALGORITHM = algorithm
        self.security = HTTPBearer()

    @staticmethod
    async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        secret = "your-super-secret-key"
        algorithm: str = "HS256"

        token = credentials.credentials
        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm])
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

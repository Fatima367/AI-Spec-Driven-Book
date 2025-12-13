"""
Authentication Middleware for verifying user sessions
"""
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from typing import Optional
import uuid

# JWT token settings
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-secret-key-here-make-it-long-and-random")
ALGORITHM = "HS256"

security = HTTPBearer(auto_error=True)

class AuthMiddleware:
    @staticmethod
    async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        """
        Verify the JWT token and return user ID if valid
        """
        token = credentials.credentials

        try:
            # Decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")

            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Could not validate credentials"
                )

            return user_id

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

    @staticmethod
    async def verify_session(request: Request) -> str:
        """
        Verify user session from request headers
        """
        authorization = request.headers.get("authorization")

        if not authorization:
            raise HTTPException(
                status_code=401,
                detail="Authorization header required"
            )

        # Check for Bearer token format
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization header format"
            )

        token = authorization.replace("Bearer ", "")

        try:
            # Decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")

            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Could not validate credentials"
                )

            return user_id

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

# Convenience function to get current user ID
async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get current user ID from JWT token
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
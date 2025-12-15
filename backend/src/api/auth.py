from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
import os
from typing import Optional
from datetime import datetime, timedelta, timezone
import uuid # For placeholder session IDs
from ..models import (
    UserRegistrationRequest,
    LoginRequest,
    UserProfileResponse,
    UpdateBackgroundRequest,
    AuthResponse,
    ErrorResponse
)
from ..services.auth_service import auth_service
from fastapi_limiter.depends import RateLimiter # Import RateLimiter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


class MessageResponse(BaseModel):
    message: str


@auth_router.on_event("startup")
async def startup_event():
    """Create required tables on startup."""
    auth_service.create_tables()


from fastapi import Form, Body
import json

@auth_router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(request: Request):
    """Register a new user with background information."""
    try:
        # Parse JSON body manually to get raw data
        body = await request.json()
        print(f"Raw signup request data: {body}")  # Debug logging

        # Create the user data manually to bypass potential Pydantic issues
        from ..models import UserRegistrationRequest
        user_data = UserRegistrationRequest(**body)

        print(f"Parsed user data: {user_data}")  # Debug logging

        # Validate email format
        if "@" not in user_data.email or "." not in user_data.email:
            raise HTTPException(status_code=400, detail="Invalid email format")

        # Validate password strength (at least 8 characters and max 72 for bcrypt)
        if len(user_data.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        if len(user_data.password) > 72:
            raise HTTPException(status_code=400, detail="Password must be no more than 72 characters")

        # Clean user input by stripping whitespace
        from ..models import UserRegistrationRequest

        # Create a clean version of user_data with stripped values
        cleaned_email = user_data.email.strip() if user_data.email else user_data.email
        cleaned_first_name = (user_data.firstName or "").strip() if user_data.firstName is not None else user_data.firstName
        cleaned_last_name = (user_data.lastName or "").strip() if user_data.lastName is not None else user_data.lastName

        # Reset to None if the cleaned value is an empty string after stripping
        cleaned_first_name = cleaned_first_name if cleaned_first_name else None
        cleaned_last_name = cleaned_last_name if cleaned_last_name else None

        cleaned_user_data = UserRegistrationRequest(
            email=cleaned_email,
            password=user_data.password,
            firstName=cleaned_first_name,
            lastName=cleaned_last_name,
            softwareExperience=user_data.softwareExperience,
            hardwareExperience=user_data.hardwareExperience,
            technicalBackground=user_data.technicalBackground,
            primaryProgrammingLanguage=user_data.primaryProgrammingLanguage
        )

        # Use the cleaned data for the rest of the function
        user_data = cleaned_user_data

        # Validate background fields if provided
        valid_software_exp = ["beginner", "intermediate", "advanced"]
        valid_hardware_exp = ["beginner", "intermediate", "advanced"]
        valid_tech_background = ["computer_science", "electrical_engineering", "mechanical_engineering", "other"]
        valid_programming_lang = ["python", "cpp", "javascript", "other"]

        # Check if values are not empty strings before validation
        if user_data.softwareExperience is not None and user_data.softwareExperience != "" and user_data.softwareExperience not in valid_software_exp:
            print(f"Invalid software experience: {user_data.softwareExperience}")  # Debug logging
            raise HTTPException(status_code=400, detail="Invalid software experience value")

        if user_data.hardwareExperience is not None and user_data.hardwareExperience != "" and user_data.hardwareExperience not in valid_hardware_exp:
            print(f"Invalid hardware experience: {user_data.hardwareExperience}")  # Debug logging
            raise HTTPException(status_code=400, detail="Invalid hardware experience value")

        if user_data.technicalBackground is not None and user_data.technicalBackground != "" and user_data.technicalBackground not in valid_tech_background:
            print(f"Invalid technical background: {user_data.technicalBackground}")  # Debug logging
            raise HTTPException(status_code=400, detail="Invalid technical background value")

        if user_data.primaryProgrammingLanguage is not None and user_data.primaryProgrammingLanguage != "" and user_data.primaryProgrammingLanguage not in valid_programming_lang:
            print(f"Invalid programming language: {user_data.primaryProgrammingLanguage}")  # Debug logging
            raise HTTPException(status_code=400, detail="Invalid programming language value")

        # Create the user
        user_profile = await auth_service.create_user(user_data)

        # Generate JWT access token
        access_token = auth_service.create_access_token(data={"sub": user_profile.id})

        # Return user data with JWT token in session
        session_response = {
            "id": str(uuid.uuid4()),
            "token": access_token,
            "expiresAt": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        }

        return AuthResponse(
            user=user_profile,
            session=session_response
        )
    except ValueError as e:
        if "Email already registered" in str(e):
            raise HTTPException(status_code=409, detail="Email already registered")
        else:
            print(f"ValueError: {str(e)}")  # Debug logging
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        print(f"Signup exception: {str(e)}")  # Debug logging
        raise HTTPException(status_code=500, detail=f"An error occurred during registration: {str(e)}")


@auth_router.post("/login", response_model=AuthResponse)
async def login(request: Request):
    """Authenticate user with email and password."""
    try:
        # Parse JSON body manually to get raw data
        body = await request.json()
        print(f"Raw login request data: {body}")  # Debug logging

        # Create the login data manually to bypass potential Pydantic issues
        from ..models import LoginRequest
        login_data = LoginRequest(**body)

        # Validate email format
        if "@" not in login_data.email or "." not in login_data.email:
            raise HTTPException(status_code=400, detail="Invalid email format")

        # Authenticate the user
        user_profile = await auth_service.authenticate_user(login_data.email, login_data.password)

        if not user_profile:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Generate JWT access token
        access_token = auth_service.create_access_token(data={"sub": user_profile.id})

        # Return user data with JWT token in session
        session_response = {
            "id": str(uuid.uuid4()),
            "token": access_token,
            "expiresAt": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        }

        return AuthResponse(
            user=user_profile,
            session=session_response
        )
    except Exception as e:
        print(f"Login exception: {str(e)}")  # Debug logging
        raise HTTPException(status_code=500, detail=f"An error occurred during login: {str(e)}")


@auth_router.post("/logout", response_model=MessageResponse)
async def logout():
    """End the current user session."""
    try:
        # Since we don't have a current user dependency without auth,
        # we'll just return success for now
        # In a real implementation, you'd track tokens and invalidate them
        return MessageResponse(message="Successfully logged out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during logout: {str(e)}")

from fastapi import Header, HTTPException
import re

@auth_router.get("/profile", response_model=UserProfileResponse)
async def get_profile(request: Request, authorization: str = Header(None)):
    """Get current user's profile with background information."""
    try:
        # Extract token from Authorization header
        if not authorization:
            raise HTTPException(status_code=401, detail="Authentication required")

        # Check for Bearer token format
        token_match = re.match(r"Bearer\s+(.+)", authorization, re.IGNORECASE)
        if not token_match:
            raise HTTPException(status_code=401, detail="Invalid authorization header format")

        token = token_match.group(1)

        # Get user from token
        user_profile = await auth_service.get_current_user_by_token(token)
        if not user_profile:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return user_profile
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication required")

@auth_router.put("/profile", response_model=UserProfileResponse)
async def update_profile(request: Request):
    """Update user's profile information (e.g., first name, last name, image)."""
    # For now, we'll return an error since we can't identify the current user
    # without proper authentication
    raise HTTPException(status_code=401, detail="Authentication required")

@auth_router.put("/profile/background", response_model=UserProfileResponse)
async def update_background(request: Request):
    """Update only the user's background information."""
    # For now, we'll return an error since we can't identify the current user
    # without proper authentication
    raise HTTPException(status_code=401, detail="Authentication required")
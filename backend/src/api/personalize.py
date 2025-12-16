from fastapi import APIRouter, Depends, HTTPException, Request, Header
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from ..services.auth_service import auth_service
from ..models import UserProfileResponse
from ..services.personalization_service import personalization_service

personalize_router = APIRouter(prefix="/personalize", tags=["personalization"])

class PersonalizationRequest(BaseModel):
    chapter_id: Optional[str] = None  # Optional since it's passed in the URL path
    user_preferences: Optional[dict] = None

class PersonalizationResponse(BaseModel):
    success: bool
    content: str
    message: str
    error: Optional[str] = None


@personalize_router.post("/{chapter_id:path}", response_model=PersonalizationResponse)
async def personalize_content(
    chapter_id: str,
    request: PersonalizationRequest,
    authorization: str = Header(None)
):
    """Personalize chapter content based on user profile and preferences.
    The chapter_id can include slashes for nested paths (e.g., part1/chapter1.1).
    """
    # Validate authentication
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    token = authorization.replace("Bearer ", "")

    # Check if token is expired first
    if auth_service.is_token_expired(token):
        raise HTTPException(status_code=401, detail="Token has expired. Please re-authenticate.")

    user_id = auth_service.decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Get user profile
    user_profile = await auth_service.get_user_profile(uuid.UUID(user_id))
    if not user_profile:
        raise HTTPException(status_code=401, detail="User not found")

    # Apply personalization logic based on user profile
    # This would involve content adaptation based on software/hardware experience
    # and other user preferences
    try:
        # Use the chapter_id from the URL path, not from the request body
        personalized_content = await personalization_service.personalize_content(
            chapter_id,
            user_profile,
            request.user_preferences
        )

        return PersonalizationResponse(
            success=True,
            content=personalized_content,
            message="Content personalized successfully"
        )
    except ValueError as ve:
        # Handle session expiration specifically
        if "session has expired" in str(ve).lower():
            raise HTTPException(status_code=401, detail="Session has expired. Please re-authenticate.")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid request: {str(ve)}")
    except Exception as e:
        # Log the error for debugging
        import traceback
        import logging
        logging.error(f"Error in personalize_content: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to personalize content: {str(e)}")


@personalize_router.get("/profile", response_model=dict)
async def get_personalization_profile(authorization: str = Header(None)):
    """Get user's personalization profile."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    token = authorization.replace("Bearer ", "")
    user_id = auth_service.decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_profile = await auth_service.get_user_profile(uuid.UUID(user_id))
    if not user_profile:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "learning_mode": getattr(user_profile, 'learning_mode', 'beginner'),
        "difficulty_level": getattr(user_profile, 'difficulty_level', 'basic'),
        "focus_area": getattr(user_profile, 'focus_area', 'theory'),
        "software_experience": getattr(user_profile, 'softwareExperience', ''),
        "hardware_experience": getattr(user_profile, 'hardwareExperience', ''),
        "technical_background": getattr(user_profile, 'technicalBackground', '')
    }
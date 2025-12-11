"""
Test script for authentication functionality
This script tests the authentication service implemented in the FastAPI backend
"""
import asyncio
from sqlmodel import SQLModel
from src.services.auth_service import AuthService
from src.models import UserRegistrationRequest
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


# Use test database URL
TEST_DATABASE_URL = "sqlite:///./test_auth.db"  # Using SQLite for tests


async def test_auth_service():
    """Test the authentication service functionality"""

    # Initialize auth service with test database
    auth_service = AuthService(TEST_DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"))

    # Create tables
    await auth_service.create_tables()

    # Test user registration
    user_data = UserRegistrationRequest(
        email="test@example.com",
        password="securepassword123",
        firstName="Test",
        lastName="User",
        softwareExperience="intermediate",
        hardwareExperience="beginner",
        technicalBackground="computer_science",
        primaryProgrammingLanguage="python"
    )

    # Create user
    user_profile = await auth_service.create_user(user_data)
    print(f"Created user: {user_profile.email}")

    # Test login
    login_result = await auth_service.authenticate_user("test@example.com", "securepassword123")
    assert login_result is not None
    print(f"Login successful for: {login_result.email}")

    # Test session creation
    session_id = await auth_service.create_session(uuid.UUID(login_result.id))
    assert session_id is not None
    print(f"Session created: {session_id}")

    # Test session validation
    user_id = await auth_service.validate_session(session_id)
    assert user_id is not None
    print(f"Session validation successful: {user_id}")

    # Test profile retrieval
    profile = await auth_service.get_user_profile(user_id)
    assert profile is not None
    assert profile.email == "test@example.com"
    print(f"Profile retrieved: {profile.email}")

    # Test background update
    from src.models import UpdateBackgroundRequest
    background_update = UpdateBackgroundRequest(
        softwareExperience="advanced",
        hardwareExperience="intermediate"
    )
    updated_profile = await auth_service.update_user_background(user_id, background_update)
    assert updated_profile is not None
    assert updated_profile.softwareExperience == "advanced"
    print(f"Background updated: {updated_profile.softwareExperience}")

    print("All authentication tests passed!")


if __name__ == "__main__":
    asyncio.run(test_auth_service())
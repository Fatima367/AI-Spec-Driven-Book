#!/usr/bin/env python3
"""
Test script to verify the complete registration flow with background questions.
This script tests the authentication service with user background data collection.
"""

import asyncio
import os
from datetime import datetime
from typing import Optional
import uuid

# Import the auth service to test the registration flow
from backend.src.services.auth_service import AuthService
from backend.src.models import UserRegistrationRequest, UpdateBackgroundRequest, UserProfileResponse


async def test_complete_registration_flow():
    """Test the complete registration flow with background questions."""
    print("Testing complete registration flow with background questions...")

    # Initialize the auth service with a test SQLite database
    database_url = "sqlite:///./test_auth.db"
    auth_service = AuthService(database_url)

    # Create tables
    auth_service.create_tables()

    # Create test user data with background information
    test_user_data = UserRegistrationRequest(
        email="testuser@example.com",
        password="SecurePass123!",
        firstName="Test",
        lastName="User",
        softwareExperience="intermediate",
        hardwareExperience="beginner",
        technicalBackground="computer_science",
        primaryProgrammingLanguage="python"
    )

    print(f"Attempting to register user: {test_user_data.email}")

    try:
        # Test registration with background questions
        user_profile = await auth_service.create_user(test_user_data)
        print(f"✓ User registered successfully: {user_profile.email}")
        print(f"  - Software Experience: {user_profile.softwareExperience}")
        print(f"  - Hardware Experience: {user_profile.hardwareExperience}")
        print(f"  - Technical Background: {user_profile.technicalBackground}")
        print(f"  - Programming Language: {user_profile.primaryProgrammingLanguage}")
        print(f"  - Background Completed: {user_profile.backgroundCompleted}")

        # Verify the user was created with the correct background data
        assert user_profile.email == test_user_data.email
        assert user_profile.softwareExperience == test_user_data.softwareExperience
        assert user_profile.hardwareExperience == test_user_data.hardwareExperience
        assert user_profile.technicalBackground == test_user_data.technicalBackground
        assert user_profile.primaryProgrammingLanguage == test_user_data.primaryProgrammingLanguage
        assert user_profile.backgroundCompleted is True  # Since background data was provided

        # Test login with the created user
        print(f"\nTesting login for user: {test_user_data.email}")
        logged_in_user = await auth_service.authenticate_user(test_user_data.email, test_user_data.password)

        if logged_in_user:
            print(f"✓ User logged in successfully: {logged_in_user.email}")
            print(f"  - Software Experience: {logged_in_user.softwareExperience}")
            print(f"  - Hardware Experience: {logged_in_user.hardwareExperience}")
            print(f"  - Technical Background: {logged_in_user.technicalBackground}")
            print(f"  - Background Completed: {logged_in_user.backgroundCompleted}")

            # Verify the logged-in user has the same background data
            assert logged_in_user.softwareExperience == test_user_data.softwareExperience
            assert logged_in_user.hardwareExperience == test_user_data.hardwareExperience
            assert logged_in_user.technicalBackground == test_user_data.technicalBackground
            assert logged_in_user.primaryProgrammingLanguage == test_user_data.primaryProgrammingLanguage
        else:
            print("✗ Login failed")
            return False

        # Test updating background information
        print(f"\nTesting background update for user: {test_user_data.email}")
        update_data = UpdateBackgroundRequest(
            softwareExperience="advanced",
            hardwareExperience="intermediate",
            technicalBackground="electrical_engineering",
            primaryProgrammingLanguage="cpp"
        )

        updated_profile = await auth_service.update_user_background(uuid.UUID(logged_in_user.id), update_data)

        if updated_profile:
            print(f"✓ Background updated successfully")
            print(f"  - New Software Experience: {updated_profile.softwareExperience}")
            print(f"  - New Hardware Experience: {updated_profile.hardwareExperience}")
            print(f"  - New Technical Background: {updated_profile.technicalBackground}")
            print(f"  - New Programming Language: {updated_profile.primaryProgrammingLanguage}")

            # Verify the background was updated
            assert updated_profile.softwareExperience == "advanced"
            assert updated_profile.hardwareExperience == "intermediate"
            assert updated_profile.technicalBackground == "electrical_engineering"
            assert updated_profile.primaryProgrammingLanguage == "cpp"
        else:
            print("✗ Background update failed")
            return False

        # Test getting user profile
        print(f"\nTesting profile retrieval for user: {test_user_data.email}")
        retrieved_profile = await auth_service.get_user_profile(uuid.UUID(logged_in_user.id))

        if retrieved_profile:
            print(f"✓ Profile retrieved successfully")
            print(f"  - Email: {retrieved_profile.email}")
            print(f"  - Software Experience: {retrieved_profile.softwareExperience}")
            print(f"  - Background Completed: {retrieved_profile.backgroundCompleted}")

            # Verify the profile data is correct
            assert retrieved_profile.email == test_user_data.email
            assert retrieved_profile.softwareExperience == "advanced"  # Updated value
            assert retrieved_profile.hardwareExperience == "intermediate"  # Updated value
        else:
            print("✗ Profile retrieval failed")
            return False

        print("\n✓ All registration flow tests passed!")
        return True

    except Exception as e:
        print(f"✗ Registration flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_registration_without_background():
    """Test registration without background questions (optional fields)."""
    print("\nTesting registration without background questions...")

    # Initialize the auth service with a test SQLite database
    database_url = "sqlite:///./test_auth2.db"
    auth_service = AuthService(database_url)

    # Create tables
    auth_service.create_tables()

    # Create test user data without background information
    test_user_data = UserRegistrationRequest(
        email="testuser2@example.com",
        password="SecurePass123!",
        firstName="Test",
        lastName="User2",
        softwareExperience=None,  # Not provided
        hardwareExperience=None,  # Not provided
        technicalBackground=None,  # Not provided
        primaryProgrammingLanguage=None  # Not provided
    )

    print(f"Attempting to register user without background: {test_user_data.email}")

    try:
        # Test registration without background questions
        user_profile = await auth_service.create_user(test_user_data)
        print(f"✓ User registered successfully: {user_profile.email}")
        print(f"  - Background Completed: {user_profile.backgroundCompleted}")

        # For this test, backgroundCompleted might be False if no background data was provided
        # But based on the logic in the service, it might still be True if any field was provided (even as None)
        # Let's check what happens
        print(f"  - Software Experience: {user_profile.softwareExperience}")
        print(f"  - Hardware Experience: {user_profile.hardwareExperience}")

        print("✓ Registration without background test completed!")
        return True

    except Exception as e:
        print(f"✗ Registration without background test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all registration flow tests."""
    print("Starting BetterAuth Registration Flow Tests\n")

    success1 = await test_complete_registration_flow()
    success2 = await test_registration_without_background()

    if success1 and success2:
        print("\n🎉 All registration flow tests completed successfully!")
    else:
        print("\n❌ Some tests failed.")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
import uuid
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from jose import JWTError, jwt
import secrets

from ..models import UserProfileResponse, UserRegistrationRequest, UpdateBackgroundRequest

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token settings
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-secret-key-here-make-it-long-and-random")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SQLAlchemy setup
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "auth_user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    software_experience = Column(String, nullable=True, default="beginner")
    hardware_experience = Column(String, nullable=True, default="beginner")
    technical_background = Column(String, nullable=True, default="other")
    primary_programming_language = Column(String, nullable=True)
    background_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class AuthService:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        """Create database tables."""
        Base.metadata.create_all(bind=self.engine)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        try:
            import bcrypt
            # Encode the password to bytes before verifying
            password_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except ImportError:
            # Fallback to passlib if bcrypt fails
            return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password."""
        # Truncate password to 72 bytes to comply with bcrypt limitations
        truncated_password = password[:72] if len(password) > 72 else password
        # Use raw bcrypt to avoid version checking issues
        try:
            import bcrypt
            # Encode the password to bytes before hashing
            password_bytes = truncated_password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            return hashed.decode('utf-8')
        except ImportError:
            # Fallback to passlib if bcrypt fails
            # Truncate password to 72 bytes to comply with bcrypt limitations
            truncated_password = truncated_password[:72] if len(truncated_password) > 72 else truncated_password
            return pwd_context.hash(truncated_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def create_user(self, user_data: UserRegistrationRequest) -> UserProfileResponse:
        """Create a new user with background information."""
        db = self.SessionLocal()
        try:
            # Check if user already exists
            existing_user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
            if existing_user:
                raise ValueError("Email already registered")

            # Hash the password
            hashed_password = self.get_password_hash(user_data.password)

            # Handle empty strings by converting them to None
            def clean_optional_field(field_value):
                return field_value if field_value != "" else None

            # Process fields, handling empty strings
            cleaned_first_name = clean_optional_field(user_data.firstName)
            cleaned_last_name = clean_optional_field(user_data.lastName)
            cleaned_software_experience = clean_optional_field(user_data.softwareExperience) or "beginner"
            cleaned_hardware_experience = clean_optional_field(user_data.hardwareExperience) or "beginner"
            cleaned_technical_background = clean_optional_field(user_data.technicalBackground) or "other"
            cleaned_primary_programming_language = clean_optional_field(user_data.primaryProgrammingLanguage)

            # Determine if background is completed
            background_completed = bool(
                cleaned_software_experience or
                cleaned_hardware_experience or
                cleaned_technical_background or
                cleaned_primary_programming_language
            )

            # Create new user
            db_user = UserDB(
                email=user_data.email,
                password=hashed_password,
                first_name=cleaned_first_name,
                last_name=cleaned_last_name,
                software_experience=cleaned_software_experience,
                hardware_experience=cleaned_hardware_experience,
                technical_background=cleaned_technical_background,
                primary_programming_language=cleaned_primary_programming_language,
                background_completed=background_completed
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            # Convert to UserProfileResponse
            return UserProfileResponse(
                id=str(db_user.id),
                email=db_user.email,
                firstName=db_user.first_name,
                lastName=db_user.last_name,
                softwareExperience=db_user.software_experience,
                hardwareExperience=db_user.hardware_experience,
                technicalBackground=db_user.technical_background,
                primaryProgrammingLanguage=db_user.primary_programming_language,
                backgroundCompleted=db_user.background_completed,
                createdAt=db_user.created_at,
                updatedAt=db_user.updated_at
            )
        finally:
            db.close()

    async def authenticate_user(self, email: str, password: str) -> Optional[UserProfileResponse]:
        """Authenticate a user with email and password."""
        db = self.SessionLocal()
        try:
            db_user = db.query(UserDB).filter(UserDB.email == email).first()
            if not db_user or not self.verify_password(password, db_user.password):
                return None

            return UserProfileResponse(
                id=str(db_user.id),
                email=db_user.email,
                firstName=db_user.first_name,
                lastName=db_user.last_name,
                softwareExperience=db_user.software_experience,
                hardwareExperience=db_user.hardware_experience,
                technicalBackground=db_user.technical_background,
                primaryProgrammingLanguage=db_user.primary_programming_language,
                backgroundCompleted=db_user.background_completed,
                createdAt=db_user.created_at,
                updatedAt=db_user.updated_at
            )
        finally:
            db.close()

    async def get_user_profile(self, user_id: uuid.UUID) -> Optional[UserProfileResponse]:
        """Get user profile by user ID."""
        db = self.SessionLocal()
        try:
            db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
            if not db_user:
                return None

            return UserProfileResponse(
                id=str(db_user.id),
                email=db_user.email,
                firstName=db_user.first_name,
                lastName=db_user.last_name,
                softwareExperience=db_user.software_experience,
                hardwareExperience=db_user.hardware_experience,
                technicalBackground=db_user.technical_background,
                primaryProgrammingLanguage=db_user.primary_programming_language,
                backgroundCompleted=db_user.background_completed,
                createdAt=db_user.created_at,
                updatedAt=db_user.updated_at
            )
        finally:
            db.close()

    def decode_access_token(self, token: str):
        """Decode and verify a JWT access token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None

    async def get_current_user_by_token(self, token: str) -> Optional[UserProfileResponse]:
        """Get user profile by token."""
        user_id = self.decode_access_token(token)
        if user_id is None:
            return None
        return await self.get_user_profile(uuid.UUID(user_id))

    async def update_user_background(self, user_id: uuid.UUID, background_data: UpdateBackgroundRequest) -> Optional[UserProfileResponse]:
        """Update user background information."""
        db = self.SessionLocal()
        try:
            db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
            if not db_user:
                return None

            # Update fields if provided
            if background_data.softwareExperience is not None:
                db_user.software_experience = background_data.softwareExperience
            if background_data.hardwareExperience is not None:
                db_user.hardware_experience = background_data.hardwareExperience
            if background_data.technicalBackground is not None:
                db_user.technical_background = background_data.technicalBackground
            if background_data.primaryProgrammingLanguage is not None:
                db_user.primary_programming_language = background_data.primaryProgrammingLanguage

            # Mark background as completed if not already
            db_user.background_completed = True

            db_user.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(db_user)

            return UserProfileResponse(
                id=str(db_user.id),
                email=db_user.email,
                firstName=db_user.first_name,
                lastName=db_user.last_name,
                softwareExperience=db_user.software_experience,
                hardwareExperience=db_user.hardware_experience,
                technicalBackground=db_user.technical_background,
                primaryProgrammingLanguage=db_user.primary_programming_language,
                backgroundCompleted=db_user.background_completed,
                createdAt=db_user.created_at,
                updatedAt=db_user.updated_at
            )
        finally:
            db.close()


# Create a global instance of the auth service
auth_service = AuthService(os.getenv("DATABASE_URL", "sqlite:///./auth.db"))

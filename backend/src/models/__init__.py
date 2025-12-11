from pydantic import BaseModel
from typing import Optional, List
from typing import Any, Dict
from datetime import datetime


class DocumentChunk(BaseModel):
    """
    A segment of the textbook content, typically Markdown, tokenized and embedded.
    """
    page_content: str
    chapter_title: str
    url_slug: str
    embedding: Optional[List[float]] = None  # Vector representation of the content
    doc_id: Optional[str] = None  # Unique identifier for the document
    chunk_id: Optional[str] = None  # Unique identifier for the chunk


class UserQuery(BaseModel):
    """
    The natural language question submitted by the user to the chatbot.
    """
    query: str
    user_id: Optional[str] = None
    selected_text: Optional[str] = None  # Specific text highlighted by user to narrow context


class ChatResponse(BaseModel):
    """
    Response from the chatbot with answer and citations.
    """
    answer: str
    citations: List[Dict[str, Any]]  # List of citations with doc_id, chunk_id, url


class QueryResponse(BaseModel):
    """
    Response from the direct query endpoint.
    """
    page_content: str
    chapter_title: str
    url_slug: str


class UserRegistrationRequest(BaseModel):
    """
    Request model for user registration with background information.
    """
    email: str
    password: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    softwareExperience: Optional[str] = "beginner"  # beginner, intermediate, advanced
    hardwareExperience: Optional[str] = "beginner"  # beginner, intermediate, advanced
    technicalBackground: Optional[str] = "other"  # computer_science, electrical_engineering, mechanical_engineering, other
    primaryProgrammingLanguage: Optional[str] = None  # python, cpp, javascript, other


class UserProfileResponse(BaseModel):
    """
    Response model for user profile with background information.
    """
    id: str
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    softwareExperience: str  # beginner, intermediate, advanced
    hardwareExperience: str  # beginner, intermediate, advanced
    technicalBackground: str  # computer_science, electrical_engineering, mechanical_engineering, other
    primaryProgrammingLanguage: Optional[str] = None  # python, cpp, javascript, other
    backgroundCompleted: bool
    createdAt: datetime
    updatedAt: datetime


class UpdateBackgroundRequest(BaseModel):
    """
    Request model for updating user background information.
    """
    softwareExperience: Optional[str] = None  # beginner, intermediate, advanced
    hardwareExperience: Optional[str] = None  # beginner, intermediate, advanced
    technicalBackground: Optional[str] = None  # computer_science, electrical_engineering, mechanical_engineering, other
    primaryProgrammingLanguage: Optional[str] = None  # python, cpp, javascript, other


class LoginRequest(BaseModel):
    """
    Request model for user login.
    """
    email: str
    password: str


class AuthResponse(BaseModel):
    """
    Response model for authentication operations.
    """
    user: UserProfileResponse
    session: Optional[dict] = None  # Session information


class ValidationErrorDetail(BaseModel):
    """
    Detail model for validation errors.
    """
    field: str
    message: str


class ErrorResponse(BaseModel):
    """
    Response model for error cases.
    """
    error: str
    message: str
    details: Optional[List[ValidationErrorDetail]] = None


class QueryResponse(BaseModel):
    """
    Response from the direct query endpoint.
    """
    page_content: str
    chapter_title: str
    url_slug: str
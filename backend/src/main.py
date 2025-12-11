from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .api import ingest, query, chat
from .api.auth import auth_router
from dotenv import load_dotenv
import os
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis # Using async Redis client
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

load_dotenv()


app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG chatbot that answers questions based on book content",
    version="1.0.0"
)

origins = [
    "https://physical-ai-n-humanoid-robotics.vercel.app",  # Without trailing slash
    "https://physical-ai-n-humanoid-robotics.vercel.app/", # With trailing slash
    "http://localhost:3000",  # For local development
    "http://127.0.0.1:3000",  # For local development
    "http://localhost:8000",  # Added for direct access
    "http://127.0.0.1:8000"   # Added for direct access
]

# Create a custom middleware for security headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # CSP should be carefully configured based on application needs, omitting for simplicity
        # response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only add HTTPS redirect middleware in production
import os
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Add a startup event handler for FastAPILimiter
@app.on_event("startup")
async def startup_event():
    try:
        # Initialize Redis client for rate limiting
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        r = redis.from_url(redis_url, encoding="utf8", decode_responses=True)
        await FastAPILimiter.init(r)
    except Exception as e:
        print(f"Warning: Could not initialize Redis for rate limiting: {e}")
        print("Rate limiting will be disabled.")


# Include API routes
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
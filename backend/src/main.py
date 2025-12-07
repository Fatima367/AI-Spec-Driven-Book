import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Import routers inside the app creation to avoid potential import issues
def create_app():
    app = FastAPI(
        title="RAG Chatbot API",
        description="API for the RAG chatbot that answers questions based on book content",
        version="1.0.0"
    )

    # Allow all origins during development, restrict in production
    origins = [
        "https://physical-ai-n-humanoid-robotics.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import and include routers inside the function to avoid potential import issues
    from .api import ingest, query, chat

    app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
    app.include_router(query.router, prefix="/api/v1", tags=["query"])
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

    @app.get("/")
    async def root():
        return {"message": "RAG Chatbot API is running!"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()

# Important for Vercel!
handler = Mangum(app)
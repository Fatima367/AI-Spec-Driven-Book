from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import ingest, query, chat


app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG chatbot that answers questions based on book content",
    version="1.0.0"
)

# Configure CORS for production deployment
origins = [
    "https://physical-ai-humanoid-robotics-textbook.vercel.app",  # Original production URL
    "https://physical-ai-n-humanoid-robotics.vercel.app",  # Alternative production URL
    "http://localhost:3000",  # Local Docusaurus frontend
    "http://localhost:3001",  # Alternative local frontend
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Allow credentials for better user tracking if needed
    allow_credentials=True,
)

# Include API routes with proper versioning
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Required for Vercel deployment


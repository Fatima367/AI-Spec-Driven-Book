from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import ingest, query, chat
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG chatbot that answers questions based on book content",
    version="1.0.0"
)

origins = [
    "https://physical-ai-n-humanoid-robotics.vercel.app/",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
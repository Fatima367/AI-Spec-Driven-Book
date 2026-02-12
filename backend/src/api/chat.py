import traceback
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from groq import Groq
import os
from dotenv import load_dotenv

from ..services.embedding_service import get_embeddings
from ..services.qdrant_service import get_qdrant_client
from .ingest import DocumentChunk

load_dotenv()

router = APIRouter()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------
# Models
# -------------------------

class Citation(BaseModel):
    doc_id: str
    chunk_id: str
    url: str

class ChatRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = []


# -------------------------
# Utility: Clean Context
# -------------------------

def clean_context(text: str) -> str:
    """
    Remove markdown, frontmatter, JSX components,
    and Docusaurus formatting before sending to LLM.
    """
    # Remove frontmatter (--- title ---)
    text = re.sub(r"---.*?---", "", text, flags=re.DOTALL)

    # Remove import lines
    text = re.sub(r"import .*", "", text)

    # Remove JSX components like <PersonalizeButton />
    text = re.sub(r"<.*?>", "", text)

    # Remove ::: blocks (tip, danger, etc.)
    text = re.sub(r":::[\s\S]*?:::", "", text)

    # Remove markdown symbols
    text = re.sub(r"[#>*`]", "", text)

    # Remove extra whitespace
    text = re.sub(r"\n\s*\n", "\n\n", text)

    return text.strip()


# -------------------------
# Chat Endpoint
# -------------------------

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    try:
        # -------------------------
        # 1️⃣ Basic Query Guard
        # -------------------------
        if len(request.query.strip().split()) < 3:
            return ChatResponse(
                answer="Hi, there. Please ask a question related to the book's content.",
                citations=[]
            )

        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks"

        if not qdrant_client.collection_exists(collection_name=collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Qdrant collection '{collection_name}' not found. Please ingest documents first."
            )

        # -------------------------
        # 2️⃣ Create Embedding
        # -------------------------
        retrieval_query_text = request.selected_text if request.selected_text else request.query
        query_embedding = get_embeddings([retrieval_query_text])[0]

        # -------------------------
        # 3️⃣ Retrieve Top Chunks
        # -------------------------
        search_result = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=2,  # Reduced from 3 to prevent token overflow
            with_payload=True
        )

        context_chunks: List[DocumentChunk] = []
        citations: List[Citation] = []

        if search_result.points:
            for scored_point in search_result.points:
                if scored_point.payload:
                    chunk = DocumentChunk(**scored_point.payload)

                    context_chunks.append(chunk)

                    citations.append(Citation(
                        doc_id=chunk.chapter_title,
                        chunk_id=f"{chunk.url_slug}-{scored_point.id}",
                        url=f"/docs{chunk.url_slug}"
                    ))

        # -------------------------
        # 4️⃣ Build Clean Context
        # -------------------------
        context_text = "\n\n".join([
            clean_context(chunk.page_content)
            for chunk in context_chunks
        ])

        if not context_text:
            return ChatResponse(
                answer="I apologize, but I couldn't find relevant information in the book.",
                citations=[]
            )

        # -------------------------
        # 5️⃣ HARD TOKEN SAFETY LIMIT
        # -------------------------
        MAX_CONTEXT_CHARS = 12000  # ~3000 tokens approx
        context_text = context_text[:MAX_CONTEXT_CHARS]

        # -------------------------
        # 6️⃣ Construct Prompt
        # -------------------------
        prompt_messages = [
            {
                "role": "system",
                "content": "You are a helpful book assistant. Answer only from the provided context. If the answer is not in the context, say you cannot answer."
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {request.query}"
            }
        ]

        # -------------------------
        # 7️⃣ Call Groq
        # -------------------------
        chat_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=prompt_messages,
            temperature=0.5,
            max_tokens=500
        )

        answer = chat_response.choices[0].message.content

        return ChatResponse(answer=answer, citations=citations)

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error.")

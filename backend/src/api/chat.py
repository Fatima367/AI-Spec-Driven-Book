from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Tuple

from ..services.embedding_service import get_embeddings, get_gemini_embedding_client
from ..services.qdrant_service import get_qdrant_client
from .ingest import DocumentChunk # Reuse DocumentChunk model

router = APIRouter()

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

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """
    Interacts with the RAG chatbot, retrieves context, and provides answers with citations.
    """
    try:
        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks"

        if not qdrant_client.collection_exists(collection_name=collection_name):
            raise HTTPException(status_code=404, detail=f"Qdrant collection '{collection_name}' not found. Please ingest documents first.")

        # Determine the text to use for retrieval
        retrieval_query_text = request.selected_text if request.selected_text else request.query
        
        query_embedding = get_embeddings(retrieval_query_text)

        # Retrieve relevant chunks from Qdrant
        search_result = qdrant_client.query(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=3, # Retrieve top N relevant documents for context
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
                        doc_id=chunk.chapter_title, # Using chapter_title as doc_id for now
                        chunk_id=f"{chunk.url_slug}-{scored_point.id}", # Unique ID for each chunk
                        url=f"/docs{chunk.url_slug}" # Assuming Docusaurus URL structure
                    ))

        # Construct prompt for the LLM
        context_text = "\n\n".join([chunk.page_content for chunk in context_chunks])
        
        # Check if the query is a greeting or related to the book content
        query_lower = request.query.lower().strip()
        greeting_keywords = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'how are you', 'what\'s up', 'sup', 'morning', 'afternoon', 'evening']

        is_greeting = any(greeting in query_lower for greeting in greeting_keywords)

        if is_greeting:
            # Return a friendly greeting message
            greeting_response = "Hello! I'm your Physical AI & Humanoid Robotics book assistant. I'm here to help you with questions about the book content. How can I assist you today?"
            return ChatResponse(answer=greeting_response, citations=[])
        elif not context_text:
            # Check if the query is related to the book topic
            book_related_keywords = ['physical ai', 'humanoid robotics', 'robot', 'ai', 'artificial intelligence', 'machine learning', 'ros2', 'digital twin', 'ai robot', 'vla', 'vision language action', 'hardware', 'software', 'capstone', 'module', 'chapter', 'textbook', 'book', 'learning', 'education', 'course', 'topic']

            is_book_related = any(keyword in query_lower for keyword in book_related_keywords)

            if not is_book_related:
                return ChatResponse(answer="I apologize, but I can only respond to greetings and queries related to Physical AI & Humanoid Robotics content. Please ask a question related to the book's content.", citations=[])
            else:
                return ChatResponse(answer="I apologize, but I couldn't find any relevant information in the book to answer your question. Please try rephrasing or ask a more specific question about the book's content.", citations=[])


        prompt_messages = [
            {"role": "system", "content": "You are a helpful book assistant. Answer the user's question ONLY based on the provided context from the book. If the question cannot be answered from the context, politely state that you cannot answer it and suggest asking a question related to the book's content. Do not use outside knowledge."},
            {"role": "user", "content": f"Context from the book:\n{context_text}\n\nUser Question: {request.query}"}
        ]
        
        # Get Gemini LLM client configured via OpenAI client
        gemini_llm_client = get_gemini_embedding_client() # Reusing the same client setup, but will call chat.completions

        # For chat completion, Gemini uses models like "gemini-pro" or "gemini-1.5-pro"
        # I'll use "gemini-1.5-pro" as it's a capable model.
        # This might need adjustment based on available models via the OpenAI-compatible endpoint.
        try:
            chat_response = gemini_llm_client.chat.completions.create(
                model="gemini-1.5-pro", # Use an appropriate Gemini chat model
                messages=prompt_messages,
                temperature=0.7,
                max_tokens=500
            )
            answer = chat_response.choices[0].message.content
        except Exception as llm_error:
            # Fallback for polite refusal if LLM call fails
            print(f"LLM call failed: {llm_error}")
            return ChatResponse(answer="I apologize, but I couldn't process your request at the moment. Please try again later.", citations=[])

        return ChatResponse(answer=answer, citations=citations)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_answer_with_citations(query: str, selected_text: str = "") -> Tuple[str, List[dict]]:
    """
    Utility function to get answer with citations, used by both regular chat API and ChatKit
    Returns: (answer, citations_list)
    """
    try:
        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks"

        if not qdrant_client.collection_exists(collection_name=collection_name):
            return "I apologize, but the book content has not been ingested yet. Please try again later.", []

        # Determine the text to use for retrieval
        retrieval_query_text = selected_text if selected_text else query

        query_embedding = get_embeddings(retrieval_query_text)

        # Retrieve relevant chunks from Qdrant
        search_result = qdrant_client.query(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=3, # Retrieve top N relevant documents for context
            with_payload=True
        )

        context_chunks: List[DocumentChunk] = []
        citations: List[dict] = []

        if search_result.points:
            for scored_point in search_result.points:
                if scored_point.payload:
                    chunk = DocumentChunk(**scored_point.payload)
                    context_chunks.append(chunk)
                    citations.append({
                        "doc_id": chunk.chapter_title, # Using chapter_title as doc_id for now
                        "chunk_id": f"{chunk.url_slug}-{scored_point.id}", # Unique ID for each chunk
                        "url": f"/docs{chunk.url_slug}" # Assuming Docusaurus URL structure
                    })

        # Construct prompt for the LLM
        context_text = "\n\n".join([chunk.page_content for chunk in context_chunks])

        # Check if the query is a greeting or related to the book content
        query_lower = query.lower().strip()
        greeting_keywords = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'how are you', 'what\'s up', 'sup', 'morning', 'afternoon', 'evening']

        is_greeting = any(greeting in query_lower for greeting in greeting_keywords)

        if is_greeting:
            # Return a friendly greeting message
            greeting_response = "Hello! I'm your Physical AI & Humanoid Robotics book assistant. I'm here to help you with questions about the book content. How can I assist you today?"
            return greeting_response, []
        elif not context_text:
            # Check if the query is related to the book topic
            book_related_keywords = ['physical ai', 'humanoid robotics', 'robot', 'ai', 'artificial intelligence', 'machine learning', 'ros2', 'digital twin', 'ai robot', 'vla', 'vision language action', 'hardware', 'software', 'capstone', 'module', 'chapter', 'textbook', 'book', 'learning', 'education', 'course', 'topic']

            is_book_related = any(keyword in query_lower for keyword in book_related_keywords)

            if not is_book_related:
                return "I apologize, but I can only respond to greetings and queries related to Physical AI & Humanoid Robotics content. Please ask a question related to the book's content.", []
            else:
                return "I apologize, but I couldn't find any relevant information in the book to answer your question. Please try rephrasing or ask a more specific question about the book's content.", []

        prompt_messages = [
            {"role": "system", "content": "You are a helpful book assistant. Answer the user's question ONLY based on the provided context from the book. If the question cannot be answered from the context, politely state that you cannot answer it and suggest asking a question related to the book's content. Do not use outside knowledge."},
            {"role": "user", "content": f"Context from the book:\n{context_text}\n\nUser Question: {query}"}
        ]

        # Get Gemini LLM client configured via OpenAI client
        gemini_llm_client = get_gemini_embedding_client() # Reusing the same client setup, but will call chat.completions

        # For chat completion, Gemini uses models like "gemini-pro" or "gemini-1.5-pro"
        # I'll use "gemini-1.5-pro" as it's a capable model.
        # This might need adjustment based on available models via the OpenAI-compatible endpoint.
        try:
            chat_response = gemini_llm_client.chat.completions.create(
                model="gemini-1.5-pro", # Use an appropriate Gemini chat model
                messages=prompt_messages,
                temperature=0.7,
                max_tokens=500
            )
            answer = chat_response.choices[0].message.content
        except Exception as llm_error:
            # Fallback for polite refusal if LLM call fails
            print(f"LLM call failed: {llm_error}")
            return "I apologize, but I couldn't process your request at the moment. Please try again later.", []

        return answer, citations

    except Exception as e:
        return f"An error occurred: {str(e)}", []

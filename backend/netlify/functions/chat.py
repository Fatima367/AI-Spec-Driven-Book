import json
import uuid
from datetime import datetime
from typing import Dict, Any

# Import your existing services and models
from services.embedding_service import get_embeddings, get_gemini_embedding_client
from services.qdrant_service import get_qdrant_client
from models import DocumentChunk, Citation


def handler(event, context):
    """
    Netlify Function handler for chat endpoint
    """
    try:
        # Parse request body
        request_data = json.loads(event.get('body', '{}'))

        # Extract request parameters
        query = request_data.get('query')
        user_id = request_data.get('user_id')
        selected_text = request_data.get('selected_text')

        if not query:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Query parameter is required'})
            }

        # Your existing chat logic
        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks"

        if not qdrant_client.collection_exists(collection_name=collection_name):
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': f"Qdrant collection '{collection_name}' not found. Please ingest documents first."})
            }

        # Determine the text to use for retrieval
        retrieval_query_text = selected_text if selected_text else query

        query_embedding = get_embeddings(retrieval_query_text)

        # Retrieve relevant chunks from Qdrant
        search_result = qdrant_client.query(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=5,  # Retrieve top 5 relevant documents for context
            with_payload=True
        )

        context_chunks = []
        citations = []

        if search_result.points:
            for scored_point in search_result.points:
                if scored_point.payload:
                    chunk = DocumentChunk(**scored_point.payload)
                    context_chunks.append(chunk)
                    citations.append({
                        'doc_id': chunk.doc_id or chunk.chapter_title,
                        'chunk_id': chunk.chunk_id or str(scored_point.id),
                        'url': f"/docs{chunk.url_slug}",
                        'chapter_title': chunk.chapter_title,
                        'text_preview': chunk.page_content[:100] + "..." if len(chunk.page_content) > 100 else chunk.page_content
                    })

        # Construct prompt for the LLM
        context_text = "\n\n".join([chunk.page_content for chunk in context_chunks])

        if not context_text:
            response = {
                "answer": "I apologize, but I couldn't find any relevant information in the book to answer your question. Please try rephrasing or ask a question directly related to the book's content.",
                "citations": []
            }
        else:
            prompt_messages = [
                {"role": "system", "content": "You are a helpful book assistant. Answer the user's question ONLY based on the provided context from the book. If the question cannot be answered from the context, politely state that you cannot answer it and suggest asking a question related to the book's content. Do not use outside knowledge. Always provide citations for your answers."},
                {"role": "user", "content": f"Context from the book:\n{context_text}\n\nUser Question: {query}"}
            ]

            # Get Gemini LLM client configured via OpenAI client
            gemini_llm_client = get_gemini_embedding_client()

            try:
                chat_response = gemini_llm_client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=prompt_messages,
                    temperature=0.3,
                    max_tokens=1000
                )
                answer = chat_response.choices[0].message.content or "I couldn't generate a response."
            except Exception as llm_error:
                print(f"LLM call failed: {llm_error}")
                answer = "I apologize, but I couldn't process your request at the moment. Please try again later."

            response = {
                "answer": answer,
                "citations": citations
            }

        # Send response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response)
        }

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
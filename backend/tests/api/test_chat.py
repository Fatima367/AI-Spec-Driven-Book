import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, ANY
from main import app # Assuming main.py is in the same directory as this test file
from openai.types.chat import ChatCompletion, ChatCompletionMessage, ChatCompletionChunk, ChatCompletionMessageDelta
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_chunk import Choice as ChunkChoice
from openai.types.completion_usage import CompletionUsage


# Mock the services before importing the api module to ensure mocks are in place
@pytest.fixture(autouse=True)
def mock_services():
    with patch('api.chat.get_qdrant_client') as mock_get_qdrant_client, \
         patch('api.chat.get_embeddings') as mock_get_embeddings, \
         patch('api.chat.get_gemini_embedding_client') as mock_get_gemini_llm_client:
        
        # Mock Qdrant Client
        mock_qdrant_client = MagicMock()
        mock_get_qdrant_client.return_value = mock_qdrant_client
        mock_qdrant_client.collection_exists.return_value = True

        # Mock Qdrant search result
        mock_point = MagicMock()
        mock_point.payload = {
            "page_content": "The quick brown fox jumps over the lazy dog.",
            "chapter_title": "Animal Stories",
            "url_slug": "/docs/animal-stories"
        }
        mock_point.id = "fox-chunk-1"
        
        mock_search_result = MagicMock()
        mock_search_result.points = [mock_point]
        mock_qdrant_client.query.return_value = mock_search_result

        # Mock Embedding Service
        mock_get_embeddings.return_value = [0.1] * 3072 # Dummy embedding

        # Mock Gemini LLM Client (OpenAI client configured for Gemini)
        mock_llm_client = MagicMock()
        mock_get_gemini_llm_client.return_value = mock_llm_client

        # Mock LLM chat completion response
        mock_chat_completion_message = ChatCompletionMessage(
            role="assistant",
            content="Based on the book, the fox is quick and brown."
        )
        mock_choice = Choice(
            finish_reason="stop",
            index=0,
            message=mock_chat_completion_message,
            logprobs=None
        )
        mock_llm_response = ChatCompletion(
            id="chatcmpl-mockid",
            choices=[mock_choice],
            created=1678886400,
            model="gemini-1.5-pro",
            object="chat.completion",
            usage=CompletionUsage(completion_tokens=10, prompt_tokens=20, total_tokens=30)
        )
        mock_llm_client.chat.completions.create.return_value = mock_llm_response

        yield mock_qdrant_client, mock_get_embeddings, mock_llm_client

client = TestClient(app)

def test_chat_with_bot_success(mock_services):
    """Test successful chat interaction with context and citations."""
    mock_qdrant_client, mock_get_embeddings, mock_llm_client = mock_services
    
    response = client.post(
        "/api/v1/chat",
        json={"query": "What about the fox?"}
    )

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["answer"] == "Based on the book, the fox is quick and brown."
    assert len(json_response["citations"]) == 1
    assert json_response["citations"][0]["doc_id"] == "Animal Stories"
    assert json_response["citations"][0]["chunk_id"] == "/docs/animal-stories-fox-chunk-1"
    assert json_response["citations"][0]["url"] == "/docs/animal-stories"

    mock_get_embeddings.assert_called_once_with("What about the fox?")
    mock_qdrant_client.query.assert_called_once_with(
        collection_name="book_content_chunks",
        query_vector=[0.1] * 3072,
        limit=3,
        with_payload=True
    )
    mock_llm_client.chat.completions.create.assert_called_once()

def test_chat_with_bot_selected_text(mock_services):
    """Test chat interaction using selected text for retrieval."""
    mock_qdrant_client, mock_get_embeddings, mock_llm_client = mock_services

    selected_text = "The fox is brown"
    response = client.post(
        "/api/v1/chat",
        json={"query": "Tell me more.", "selected_text": selected_text}
    )

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["answer"] == "Based on the book, the fox is quick and brown." # LLM response is mocked
    
    mock_get_embeddings.assert_called_once_with(selected_text) # Embeddings called with selected_text
    mock_llm_client.chat.completions.create.assert_called_once()


def test_chat_with_bot_no_context_found(mock_services):
    """Test chat interaction when no relevant context is found."""
    mock_qdrant_client, mock_get_embeddings, mock_llm_client = mock_services
    mock_qdrant_client.query.return_value.points = [] # Simulate no points found

    response = client.post(
        "/api/v1/chat",
        json={"query": "What is the meaning of life?"}
    )

    assert response.status_code == 200
    json_response = response.json()
    assert "I apologize, but I couldn't find any relevant information" in json_response["answer"]
    assert len(json_response["citations"]) == 0
    mock_llm_client.chat.completions.create.assert_not_called() # LLM should not be called

def test_chat_with_bot_llm_api_error(mock_services):
    """Test chat interaction when LLM API call fails."""
    mock_qdrant_client, mock_get_embeddings, mock_llm_client = mock_services
    mock_llm_client.chat.completions.create.side_effect = Exception("LLM connection error")

    response = client.post(
        "/api/v1/chat",
        json={"query": "Tell me something."}
    )

    assert response.status_code == 200
    json_response = response.json()
    assert "I apologize, but I couldn't process your request" in json_response["answer"]
    assert len(json_response["citations"]) == 0
    mock_llm_client.chat.completions.create.assert_called_once()

def test_chat_with_bot_collection_not_found(mock_services):
    """Test chat when the Qdrant collection does not exist."""
    mock_qdrant_client, _, _ = mock_services
    mock_qdrant_client.collection_exists.return_value = False # Simulate collection not found

    response = client.post(
        "/api/v1/chat",
        json={"query": "Hello"}
    )

    assert response.status_code == 404
    assert "collection 'book_content_chunks' not found" in response.json()["detail"]
    mock_qdrant_client.collection_exists.assert_called_once_with(collection_name="book_content_chunks")
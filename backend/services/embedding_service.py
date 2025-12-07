import os
from openai import OpenAI

def get_gemini_embedding_client() -> OpenAI:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    # Use the Google Generative Language API endpoint for OpenAI compatibility
    gemini_base_url = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY must be set in environment variables")

    client = OpenAI(
        api_key=gemini_api_key,
        base_url=gemini_base_url,
    )
    return client

def get_embeddings(text: str) -> list[float]:
    client = get_gemini_embedding_client()
    # Using a common Gemini embedding model identifier
    # If this fails, try 'text-embedding-004' or consult Google's latest documentation
    model = "text-embedding-004"

    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

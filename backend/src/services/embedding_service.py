import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


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

def get_embeddings(texts: list[str]) -> list[list[float]]:
    client = get_gemini_embedding_client()
    # Using a common Gemini embedding model identifier
    # If this fails, consult Google's latest documentation
    model = "text-embedding-004" 

    response = client.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]
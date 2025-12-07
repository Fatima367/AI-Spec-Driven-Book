import json
from typing import Dict, Any

# Import your existing services and models
from services.embedding_service import get_embeddings
from services.qdrant_service import get_qdrant_client
from models import DocumentChunk


def handler(event, context):
    """
    Netlify Function handler for query endpoint
    """
    try:
        # Parse request body
        request_data = json.loads(event.get('body', '{}'))

        # Extract query parameter
        query = request_data.get('query')

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

        # Your existing query logic
        qdrant_client = get_qdrant_client()
        collection_name = "book_content_chunks"

        # Check if collection exists
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

        query_embedding = get_embeddings(query)

        search_result = qdrant_client.query(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=5,  # Limit to top 5 relevant documents
            with_payload=True  # Retrieve the full payload (DocumentChunk data)
        )

        results = []
        for scored_point in search_result.points:
            if scored_point.payload:
                # Create DocumentChunk from payload and add score
                chunk_data = scored_point.payload.copy()
                chunk_data['score'] = scored_point.score
                results.append(chunk_data)

        # Send response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(results)
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
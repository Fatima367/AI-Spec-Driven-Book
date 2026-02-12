"""
Script to delete the Qdrant collection and start fresh.
Run this before re-ingesting to avoid duplicates.
"""
import os
from dotenv import load_dotenv
from src.services.qdrant_service import get_qdrant_client

load_dotenv()

def delete_collection():
    """Delete the book_content_chunks collection."""
    try:
        client = get_qdrant_client()
        collection_name = "book_content_chunks"

        if client.collection_exists(collection_name=collection_name):
            print(f"🗑️  Deleting collection '{collection_name}'...")
            client.delete_collection(collection_name=collection_name)
            print(f"✅ Collection '{collection_name}' deleted successfully!")
            print(f"📝 You can now run ingestion to create fresh data with language tags.")
        else:
            print(f"ℹ️  Collection '{collection_name}' does not exist. Nothing to delete.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Qdrant Collection Cleanup")
    print("=" * 80)

    response = input("⚠️  This will delete ALL data in the collection. Continue? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        delete_collection()
    else:
        print("❌ Operation cancelled.")

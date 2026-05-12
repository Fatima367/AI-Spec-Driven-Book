import requests
import time

def trigger_ingestion():
    """
    Trigger the ingestion endpoint with timeout and retry logic
    """
    url = "http://localhost:8000/api/v1/ingest"

    print("Starting ingestion process...")
    print(f"Sending POST request to: {url}")

    try:
        # Set a longer timeout (10 minutes)
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            timeout=600  # 10 minutes timeout
        )

        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            print("\n✓ Ingestion completed successfully!")
        else:
            print(f"\n✗ Ingestion failed with status code: {response.status_code}")

    except requests.exceptions.Timeout:
        print("\n✗ Request timed out after 10 minutes")
    except requests.exceptions.ConnectionError as e:
        print(f"\n✗ Connection error: {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    trigger_ingestion()

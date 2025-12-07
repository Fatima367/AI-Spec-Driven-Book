import os
import pytest
from unittest.mock import MagicMock, patch
from services.qdrant_service import get_qdrant_client
from qdrant_client import QdrantClient

@patch.dict(os.environ, {"QDRANT_API_KEY": "test_key", "QDRANT_CLUSTER_URL": "http://test_url"})
def test_get_qdrant_client_success():
    """Test successful Qdrant client initialization."""
    client = get_qdrant_client()
    assert isinstance(client, QdrantClient)
    assert client.host == "test_url"
    assert client.api_key == "test_key"

@patch.dict(os.environ, {"QDRANT_API_KEY": "", "QDRANT_CLUSTER_URL": "http://test_url"})
def test_get_qdrant_client_no_api_key():
    """Test Qdrant client initialization without API key."""
    with pytest.raises(ValueError, match="QDRANT_API_KEY and QDRANT_CLUSTER_URL must be set"):
        get_qdrant_client()

@patch.dict(os.environ, {"QDRANT_API_KEY": "test_key", "QDRANT_CLUSTER_URL": ""})
def test_get_qdrant_client_no_cluster_url():
    """Test Qdrant client initialization without cluster URL."""
    with pytest.raises(ValueError, match="QDRANT_API_KEY and QDRANT_CLUSTER_URL must be set"):
        get_qdrant_client()

@patch.dict(os.environ, {}, clear=True)
def test_get_qdrant_client_no_env_vars():
    """Test Qdrant client initialization with no environment variables."""
    with pytest.raises(ValueError, match="QDRANT_API_KEY and QDRANT_CLUSTER_URL must be set"):
        get_qdrant_client()
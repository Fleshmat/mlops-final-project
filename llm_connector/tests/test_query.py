from fastapi.testclient import TestClient
import sys
import os

# ensure importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import main


def test_query_endpoint():
    client = TestClient(main.app)
    resp = client.post("/query", json={"question": "¿Cuál es la capital de Francia?"})
    assert resp.status_code in (200, 503)
    data = resp.json()
    assert isinstance(data, dict)

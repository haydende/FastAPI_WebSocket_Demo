from fastapi.testclient import TestClient
from websocketchat.websocketchat import app


def test_index_html_served():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.content != ""
        client.close()

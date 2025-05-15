from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)

def test_testar_se_teste_funciona():
    response = client.post("/teste")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
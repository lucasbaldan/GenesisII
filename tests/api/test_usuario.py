
from http import HTTPStatus
from fastapi.testclient import TestClient


def test_create_usuario_222(client: TestClient):
    response = client.post(
        "/usuarios/",
        json={
              "email": "222@gmail.com",
              "password": "123",
              "nome_completo": "lucas baldan",
              "cpf": "222",
              "celular1": "27996103528",
              "ativo": True,
              "permissoes": 
              [
                  1
              ]
            },
        )
    
    assert response.status_code == HTTPStatus.CREATED


def test_create_usuario_222_error_email_duplicate(client: TestClient):
    response = client.post(
        "/usuarios/",
        json={
              "email": "222@gmail.com",
              "password": "123",
              "nome_completo": "lucas baldan",
              "cpf": "222",
              "celular1": "27996103528",
              "ativo": True,
              "permissoes": 
              [
                  1
              ]
            },
        )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email já cadastrado na plataforma."}


def test_update_usuario_222_OK(client: TestClient):
    response = client.put(
        "/usuarios/6",
        json={
              "email": "222222@gmail.com",
              "password": "123",
              "nome_completo": "lucas baldan",
              "cpf": "22244",
              "celular1": "27996103528",
              "ativo": True,
              "permissoes": 
              [
                  1, 2
              ]
            },
        )
    
    assert response.status_code == HTTPStatus.OK

def test_update_usuario_NOT_FOUND(client: TestClient):
    response = client.put(
        "/usuarios/898",
        json={
              "email": "222222@gmail.com",
              "password": "123",
              "nome_completo": "lucas baldan",
              "cpf": "22244",
              "celular1": "27996103528",
              "ativo": True,
              "permissoes": 
              [
                  1, 2
              ]
            },
        )
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Usuário não encontrado na base de dados."}

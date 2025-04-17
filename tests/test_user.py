from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("api/v1/user", params={"email": "unexisting@mail.ru"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
    pass

def test_create_user_with_valid_email():
    already_existed = len(users)
    response = client.post("api/v1/user", json={"name": "srgold78", "email": "srgold78@mail.ru"})
    assert response.status_code == 201
    assert response.json() == already_existed + 1

def test_create_user_with_invalid_email():
    already_existed = len(users)
    response = client.post("api/v1/user", json={"name": "srgold78_1", "email": "srgold78@mail.ru"})
    assert response.status_code == 409
    assert response.json() == {'detail': 'User with this email already exists'}
    pass

def test_delete_user():
    response = client.delete("api/v1/user", params={"email": "srgold78@mail.ru"})
    assert response.status_code == 204

    response = client.get("api/v1/user", params = {"email": "srgold78@mail.ru"})
    assert response.status_code == 404
    pass

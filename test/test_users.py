import pytest
from jose import jwt

import environ
from app import schemas


def test_create_user(client):
    res = client.post('/users', json={"email": "test@example.com", "password": "testpassword"})
    new_user = schemas.UserResponse(**res.json())

    assert new_user.email == "test@example.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, environ.SK, algorithms=[environ.JTW_ALGORITHM])
    id = payload.get('user_id')

    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongmail@gmail.com', 'testtest', 403),
    ('test@example.com', 'wrongpass', 403),
    ('wrong@email.com', 'wrongpass', 403),
    (None, 'testtest', 422),
    ('test@example.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={"username": email,
                                      "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid credentials'


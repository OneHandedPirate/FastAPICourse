import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import environ
from app.database import get_db
from app.main import app
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{environ.POSTGRES_USER}:" \
                          f"{environ.POSTGRES_PASSWORD}@" \
                          f"{environ.POSTGRES_HOST}/" \
                          f"{environ.POSTGRES_DB}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# models.Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "testtest"
    }

    res = client.post("/users", json=user_data)

    new_user = res.json()
    new_user['password'] = user_data['password']

    assert res.status_code == 201

    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "test2@example.com",
        "password": "testtest"
    }

    res = client.post("/users", json=user_data)

    new_user = res.json()
    new_user['password'] = user_data['password']

    assert res.status_code == 201

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            'title': 'first title',
            'content': 'first content',
            'author_id': test_user['id']
        },
        {
            'title': 'second title',
            'content': 'second content',
            'author_id': test_user['id']
        },
        {
            'title': 'third title',
            'content': 'third content',
            'author_id': test_user['id']
        },
        {
            'title': 'third title',
            'content': 'third content',
            'author_id': test_user['id']
        },
        {
            'title': 'fourth title',
            'content': 'fourth content',
            'author_id': test_user2['id']
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)

    session.commit()

    post_query = session.query(models.Post).all()

    return post_query

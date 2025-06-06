import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app1
from httpx import AsyncClient, ASGITransport
from db.session import get_db, SessionLocal
from db.base_class import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


TEST_DATABASE_URL = "sqlite:///:memory:"
engine_test = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)

@pytest.fixture()
def client(db, monkeypatch):
    async def override_get_db():
        try:
            yield db
        finally:
            pass
    monkeypatch.setattr(get_db, "__call__", override_get_db)
    transport = ASGITransport(app=app1)
    return AsyncClient(transport=transport, base_url="http://testserver")

@pytest.mark.asyncio
async def test_register(client):
    # Test user registration
    response = await client.post("/v1/auth/register", json={
        "user_id": "20",
        "name": "testuser",
        "email": "test12@gmail.com",
        "password": "123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "testuser"
    assert data["email"] == "test12@gmail.com"
    assert "user_id" in data

@pytest.mark.asyncio
async def test_login_with_valid_credentials(client):
    # Test login with valid credentials
    response = await client.post("/v1/auth/login", data={
        "username": "test1@gmail.com",
        "password": "123"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_with_invalid_credentials(client):
    # Test login with invalid credentials
    response = await client.post("/v1/auth/login", data={
        "username": "pendeje@gmail.com",
        "password": "123"
    })
    assert response.status_code == 401
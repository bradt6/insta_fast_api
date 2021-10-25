import http
from os import stat
import pytest
from models import User
import httpx
import asyncio
from asgi_lifespan import LifespanManager
from fastapi import status
from app import app, get_database

database_test = None
def get_test_database():
    return get_database

@pytest.fixture
def user():
    return User(
        id = 1,
        first_name = "Brad",
        last_name = "T",
        email = "BradT@fakeemail.com"
    )

def test_user_id(user):
    assert user.id == 1

def test_user_first_name(user):
    assert user.first_name == "Brad"

def test_user_last_name(user):
    assert user.last_name == "T"

def test_user_email(user):
    assert user.email == "BradT@fakeemail.com"

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://localhost:8000/") as test_client:
            yield test_client

@pytest.mark.asyncio
async def test_get_user_by_id(test_client: httpx.AsyncClient):
    response = await test_client.get("/users/1")

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json == {
                    "id": 1,
                    "first_name": "Ashley",
                    "last_name": "Rhodes",
                    "email": "AshleyRhodes@fakeemail.com"
                }

@pytest.mark.asyncio
async def test_get_user_by_incorrect_id(test_client: httpx.AsyncClient):
    response = await test_client.get("/users/1")

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert not json == {
                    "id": 1,
                    "first_name": "Brad",
                    "last_name": "Rhodes",
                    "email": "AshleyRhodes@fakeemail.com"
                }

@pytest.mark.asyncio
async def test_out_of_bounds(test_client: httpx.AsyncClient):
    response = await test_client.get("/users/-1")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    json = response.json()
    assert json == {
                    "detail": "Not Found"
                    }


@pytest.mark.asyncio
async def test_db_query(test_client):
    response = await test_client.get("users?skip=0&limit=10")

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    first_10_results = [
  {
    "id": 0,
    "first_name": "George",
    "last_name": "Davis",
    "email": "GeorgeDavis@fakeemail.com"
  },
  {
    "id": 1,
    "first_name": "Ashley",
    "last_name": "Rhodes",
    "email": "AshleyRhodes@fakeemail.com"
  },
  {
    "id": 2,
    "first_name": "Brittney",
    "last_name": "Gibson",
    "email": "BrittneyGibson@fakeemail.com"
  },
  {
    "id": 3,
    "first_name": "Larry",
    "last_name": "King",
    "email": "LarryKing@fakeemail.com"
  },
  {
    "id": 4,
    "first_name": "Kimberly",
    "last_name": "Robertson",
    "email": "KimberlyRobertson@fakeemail.com"
  },
  {
    "id": 5,
    "first_name": "Kimberly",
    "last_name": "Bell",
    "email": "KimberlyBell@fakeemail.com"
  },
  {
    "id": 6,
    "first_name": "Mark",
    "last_name": "Tucker",
    "email": "MarkTucker@fakeemail.com"
  },
  {
    "id": 7,
    "first_name": "Lindsey",
    "last_name": "Hodge",
    "email": "LindseyHodge@fakeemail.com"
  },
  {
    "id": 8,
    "first_name": "Kathryn",
    "last_name": "Baker",
    "email": "KathrynBaker@fakeemail.com"
  },
  {
    "id": 9,
    "first_name": "Robert",
    "last_name": "Rogers",
    "email": "RobertRogers@fakeemail.com"
  }
]
    for i in range(10):
        assert json["data"][i] == first_10_results[i]

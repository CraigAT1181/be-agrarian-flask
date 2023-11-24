import requests
import pytest
from seed import seed_database
from urllib.parse import urljoin

path = 'http://127.0.0.1:5000'

@pytest.fixture(autouse=True)
def seed_db():
    seed_database()
    yield

def test_home_endpoint(seed_db):
    endpoint = '/'
    url = urljoin(path, endpoint)

    response=requests.get(url)
    assert response.status_code == 200

def test_get_all_produce(seed_db):
    endpoint = '/produce'
    url = urljoin(path, endpoint)

    response=requests.get(url)
    assert response.status_code == 200
    produce_list = response.json()
    required_keys = [
        "produce_id",
        "produce_name",
        "type"
        ]
    for item in produce_list["produce"]:
        if all(key in item for key in required_keys):
            pass
        else:
            raise ValueError(f'Missing required key for produce: {item}')

def test_get_users(seed_db):
    endpoint = '/users'
    url = urljoin(path, endpoint)

    response=requests.get(url)
    assert response.status_code == 200
    user_list = response.json()
    assert len(user_list["users"]) == 10
    required_keys = [
        "user_id",
        "user_name",
        "postcode",
        "produce"
        ]
    for user in user_list["users"]:
        if all(key in user for key in required_keys):
            pass
        else:
            raise ValueError(f'Missing required key for user: {user}')
        
def test_get_users_with_query(seed_db):
    endpoint = '/users?produce=Cucumber'
    url = urljoin(path, endpoint)

    response=requests.get(url)
    assert response.status_code == 200
    user_list = response.json()
    assert len(user_list["users"]) == 2
    required_keys = [
        "user_id",
        "user_name",
        "postcode",
        "produce"
        ]
    for user in user_list["users"]:
        if all(key in user for key in required_keys):
            pass
        else:
            raise ValueError(f'Missing required key for user: {user}')
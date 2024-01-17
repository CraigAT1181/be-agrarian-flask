import requests
import pytest
from seed import seed_database
from urllib.parse import urljoin

path = 'http://127.0.0.1:5000'

@pytest.fixture(autouse=True)
def seed_db():
    seed_database()
    yield

@pytest.fixture
def api_session():
    with requests.Session() as session:
        yield session

def test_get_endpoint(seed_db, api_session):
    endpoint = '/'
    url = urljoin(path, endpoint)

    response=api_session.get(url)
    assert response.status_code == 200

def test_get_all_produce(seed_db, api_session):
    endpoint = '/produce'
    url = urljoin(path, endpoint)

    response=api_session.get(url)
    assert response.status_code == 200
    produce_list = response.json()
    required_keys = [
        "produce_id",
        "produce_name",
        "produce_type",
        "produce_icon"
        ]
    for item in produce_list["produce"]:
        if not all(key in item for key in required_keys):
            raise ValueError(f'Missing required key for produce: {item}')

def test_get_all_users(seed_db, api_session):
    endpoint = '/users'
    url = urljoin(path, endpoint)

    response=api_session.get(url)
    assert response.status_code == 200
    user_list = response.json()
    assert len(user_list["users"]) == 10
    required_keys = [
        "user_id",
        "username",
        "postcode",
        "produce"
        ]
    for user in user_list["users"]:
        if not all(key in user for key in required_keys):
            raise ValueError(f'Missing required key for user: {user}')
        
def test_get_users_by_produce_name(seed_db, api_session):
    produce_list = 'Apple,Tomato'
    endpoint = f'/users/{produce_list}'
    url = urljoin(path, endpoint)

    response=api_session.get(url)
    assert response.status_code == 200
    user_list = response.json()
    assert len(user_list["users"]) == 3
    required_keys = [
        "user_id",
        "username",
        "postcode",
        "produce"
        ]
    for user in user_list["users"]:
        if not all(key in user for key in required_keys):
            raise ValueError(f'Missing required key for user: {user}')

def test_get_conversations_by_user_id(seed_db, api_session):
    user_id = 4
    endpoint = f'/users/{user_id}/conversations'
    url = urljoin(path, endpoint)

    response=api_session.get(url)
    assert response.status_code == 200
    conversation_list = response.json()
    assert len(conversation_list["conversations"]) == 2
    required_keys = [
        "conversation_id",
        "user1_id",
        "user1_username",
        "user2_id",
        "user2_username",
        "created_at"
        ]
    for conversation in conversation_list["conversations"]:
        if not all(key in conversation for key in required_keys):
            raise ValueError(f'Missing required key for user: {conversation}')
        
def test_add_conversation_by_user_id(seed_db, api_session):
    new_conversation = {
        'user2_id': '5'
    }

    endpoint = '/users/3/conversations'
    url = urljoin(path, endpoint)

    response = api_session.post(url, json=new_conversation)
    
    assert response.status_code == 200

    conversation = response.json()
    
    required_keys = ["conversation_id", "user1_id", "user2_id", "created_at"]
    assert all(key in conversation for key in required_keys)

def test_get_messages_by_conversation_id(seed_db, api_session):
    endpoint = '/conversations/1/messages'
    url = urljoin(path, endpoint)

    response=api_session.get(url)
    assert response.status_code == 200

def test_add_message_by_conversation_id(seed_db, api_session):
    new_message = {
        'sender_id': '1',
        'message': 'Testing new message.'
    }

    endpoint = '/conversations/1/messages'
    url = urljoin(path, endpoint)

    response = api_session.post(url, json=new_message)
    
    assert response.status_code == 200

    message = response.json()
    
    required_keys = ["message_id", "conversation_id", "sender_id", "message", "created_at"]
    assert all(key in message for key in required_keys)

def test_authenticate_user(seed_db, api_session):
    test_user_data = {
        'username': 'John Doe',
        'password': 'random_password_1'
    }

    endpoint = '/authenticate'
    url = urljoin(path, endpoint)

    response = api_session.post(url, json=test_user_data)
    assert response.status_code == 200

    user = response.json()
    
    required_keys = ["user_id", "username", "email", "postcode", "produce"]
    assert all(key in user for key in required_keys)

def test_add_new_user(seed_db, api_session):
    new_user = {
        'username': 'Craig Tipple',
        'email': 'craig@e-mail.com',
        'password': 'password123',
        'postcode': 'TS245EE'
    }

    endpoint = '/users'
    url = urljoin(path, endpoint)

    response = api_session.post(url, json=new_user)
    
    assert response.status_code == 200

    user = response.json()
    
    required_keys = ["user_id", "username", "email", "postcode", "produce"]
    assert all(key in user for key in required_keys)

def test_delete_user_by_user_id(seed_db, api_session):
    endpoint = '/users/10'
    url = urljoin(path, endpoint)

    response = api_session.delete(url)

    assert response.status_code == 204

def test_patch_user_produce(seed_db, api_session):
    endpoint = '/users/1'
    url = urljoin(path, endpoint)
    request = ["Apple"]

    response = api_session.patch(url, json=request)

    assert response.status_code == 200

def test_get_all_posts(seed_db, api_session):
    endpoint = '/posts'
    url = urljoin(path, endpoint)

    response=api_session.get(url)
    assert response.status_code == 200
    post_list = response.json()
    assert len(post_list["posts"]) == 10
    required_keys = [
        "post_id",
        "user_id",
        "status",
        "type",
        "image",
        "body",
        "created_at",
        "postcode",
        "posted_by"
    ]
    for post in post_list["posts"]:
        if not all(key in post for key in required_keys):
            raise ValueError(f'Missing required key for post: {post}')

def test_get_all_posts_from_search(seed_db, api_session):
    endpoint = '/posts?item=apple'
    url = urljoin(path, endpoint)

    response=api_session.get(url)
    assert response.status_code == 200
    post_list = response.json()
    required_keys = [
        "post_id",
        "user_id",
        "status",
        "type",
        "image",
        "body",
        "created_at",
        "postcode",
        "posted_by"
    ]
    for post in post_list["posts"]:
        if not all(key in post for key in required_keys):
            raise ValueError(f'Missing required key for post: {post}')
    
def test_create_post(seed_db, api_session):
    new_post = {
        'status': 'Wanted',
        'type': 'Produce',
        'item': 'Pumpkin',
        'image': '',
        'body': 'If anyone has any pumpkins, please get in touch.',
    }

    endpoint = '/posts/6'
    url = urljoin(path, endpoint)

    response = api_session.post(url, json=new_post)
    
    assert response.status_code == 200

    post = response.json()
    
    required_keys = ["post_id", "user_id", "status", "type", "item", "body", "created_at"]
    assert all(key in post for key in required_keys)

def test_delete_post_by_post_id(seed_db, api_session):
    endpoint = '/posts/1'
    url = urljoin(path, endpoint)

    response = api_session.delete(url)

    assert response.status_code == 204
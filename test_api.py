import pytest
from flask import Flask
from app import create_app, db
from app.models import User

@pytest.fixture(scope='module')
def test_client():
    app = create_app('app.config.Config')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'DEBUG': False,
        'JWT_SECRET_KEY': 'test_secret'
    })

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('password')
            db.session.add(admin)

            user1 = User(username='user1', email='user1@example.com', role='user')
            user1.set_password('password')
            db.session.add(user1)

            db.session.commit()
        yield testing_client

    with app.app_context():
        db.drop_all()

def test_token_generation(test_client):
    response = test_client.post('/api/token', json={
        'email': 'user1@example.com',
        'password': 'password'
    })

    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_hello_protected_no_token(test_client):
    response = test_client.get('/api/hello')
    assert response.status_code == 401

def test_hello_protected_with_token(test_client):
    token_response = test_client.post('/api/token', json={
        'email': 'user1@example.com',
        'password': 'password'
    })
    token = token_response.get_json()['access_token']

    response = test_client.get('/api/hello', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    assert 'message' in response.get_json()

def test_admin_only_endpoint(test_client):
    token_response = test_client.post('/api/token', json={
        'email': 'admin@example.com',
        'password': 'password'
    })
    token = token_response.get_json()['access_token']

    response = test_client.get('/api/admin-only', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Hello, Admin!'

def test_user_only_endpoint(test_client):
    token_response = test_client.post('/api/token', json={
        'email': 'user1@example.com',
        'password': 'password'
    })
    token = token_response.get_json()['access_token']

    response = test_client.get('/api/user-only', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Hello, User!'

def test_user_access_admin_only_endpoint(test_client):
    token_response = test_client.post('/api/token', json={
        'email': 'user1@example.com',
        'password': 'password'
    })
    token = token_response.get_json()['access_token']

    response = test_client.get('/api/admin-only', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 403

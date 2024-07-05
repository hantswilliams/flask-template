import pytest
from flask import Flask
from app import create_app, db
from app.models import User, Role, Permission

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

    print("test_token_generation:")
    print(f"Status Code: {response.status_code}")
    print(f"Access Token: {response.get_json().get('access_token', None)}")

def test_hello_protected_no_token(test_client):
    response = test_client.get('/api/hello')
    assert response.status_code == 401

    print("test_hello_protected_no_token:")
    print(f"Status Code: {response.status_code}")

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

    print("test_hello_protected_with_token:")
    print(f"Status Code: {response.status_code}")
    print(f"Message: {response.get_json().get('message', None)}")

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

    print("test_admin_only_endpoint:")
    print(f"Status Code: {response.status_code}")
    print(f"Message: {response.get_json().get('message', None)}")

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

    print("test_user_only_endpoint:")
    print(f"Status Code: {response.status_code}")
    print(f"Message: {response.get_json().get('message', None)}")

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

    print("test_user_access_admin_only_endpoint:")
    print(f"Status Code: {response.status_code}")

def test_create_new_user_and_role(test_client):
    # Create a new user
    user = User(username='newuser', email='newuser@example.com', role='user')
    user.set_password('newpassword')
    db.session.add(user)
    db.session.commit()

    print("User created:")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Role: {user.role}")

    # Create a new role
    role = Role(name='newrole')
    db.session.add(role)
    db.session.commit()

    print("Role created:")
    print(f"Role Name: {role.name}")

    # Assign the new role to the user
    user.role = 'newrole'
    db.session.commit()

    print("Role assigned to user:")
    print(f"Username: {user.username}")
    print(f"Assigned Role: {user.role}")

    # Set permissions for an API endpoint
    permission = Permission(
        user_id=user.id,
        endpoint='/api/new-endpoint',
        role='newrole',
        can_read=True,
        can_write=True,
        can_update=True,
        can_delete=True
    )
    db.session.add(permission)
    db.session.commit()

    print("Permissions set for user:")
    print(f"Username: {user.username}")
    print(f"Endpoint: {permission.endpoint}")
    print(f"Role: {permission.role}")
    print(f"Can Read: {permission.can_read}")
    print(f"Can Write: {permission.can_write}")
    print(f"Can Update: {permission.can_update}")
    print(f"Can Delete: {permission.can_delete}")

    # Check the permissions for the API endpoint
    assigned_permissions = Permission.query.filter_by(user_id=user.id, endpoint='/api/new-endpoint').first()
    assert assigned_permissions is not None
    assert assigned_permissions.can_read is True
    assert assigned_permissions.can_write is True
    assert assigned_permissions.can_update is True
    assert assigned_permissions.can_delete is True

    print("Permissions verification:")
    print(f"Assigned Permissions: {assigned_permissions}")


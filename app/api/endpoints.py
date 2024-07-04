from flask import Blueprint, request, jsonify, abort
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models import User
from werkzeug.security import check_password_hash
from flasgger import swag_from
from app.decorators import role_required

api = Blueprint('api', __name__)
api_restful = Api(api)
jwt = JWTManager()

class HelloWorld(Resource):
    @jwt_required()
    @swag_from({
        'responses': {
            200: {
                'description': 'A Hello World message',
                'examples': {
                    'application/json': {
                        'message': 'Hello, World!'
                    }
                }
            },
            401: {
                'description': 'Missing or invalid token',
                'examples': {
                    'application/json': {
                        'msg': 'Missing Authorization Header'
                    }
                }
            }
        }
    })
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hello, User {current_user}!'}

class TokenResource(Resource):
    @swag_from({
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {
                            'type': 'string'
                        },
                        'password': {
                            'type': 'string'
                        }
                    },
                    'required': ['email', 'password']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'A valid access token',
                'examples': {
                    'application/json': {
                        'access_token': 'your_access_token_here'
                    }
                }
            },
            400: {
                'description': 'Invalid request',
                'examples': {
                    'application/json': {
                        'message': 'Invalid request'
                    }
                }
            },
            401: {
                'description': 'Invalid credentials',
                'examples': {
                    'application/json': {
                        'message': 'Invalid credentials'
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        print('data: ', data)
        if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Invalid request'}, 400

        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=user.id, expires_delta=False)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class AdminOnlyResource(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        return {'message': 'Hello, Admin!'}

class UserOnlyResource(Resource):
    @jwt_required()
    @role_required('user')
    def get(self):
        return {'message': 'Hello, User!'}

api_restful.add_resource(HelloWorld, '/hello')
api_restful.add_resource(TokenResource, '/token')
api_restful.add_resource(AdminOnlyResource, '/admin-only')
api_restful.add_resource(UserOnlyResource, '/user-only')

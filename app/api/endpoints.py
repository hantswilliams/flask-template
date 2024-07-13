from flask import Blueprint, request, jsonify, abort
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models import User
from werkzeug.security import check_password_hash
from flasgger import swag_from
from app.decorators import dynamic_role_required

api = Blueprint('api', __name__)
api_restful = Api(api)
jwt = JWTManager()
class TokenResource(Resource):
    @swag_from({
        'summary': 'Generate API Token',
        'description': 'Generates an API token for a user with valid credentials.',
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
        if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Invalid request'}, 400

        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=user.id, expires_delta=False)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class HelloWorld(Resource):
    @jwt_required()
    @dynamic_role_required(can_read=True)
    @swag_from({
        'summary': 'Hello World',
        'description': 'Returns a Hello World message. Requires a valid JWT token.',
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
            },
            403: {
                'description': 'Forbidden: User does not have the required permission',
                'examples': {
                    'application/json': {
                        'msg': 'Read permission required'
                    }
                }
            },
            404: {
                'description': 'Not Found',
                'examples': {
                    'application/json': {
                        'message': 'Not Found'
                    }
                }
            },
            500: {
                'description': 'Internal Server Error',
                'examples': {
                    'application/json': {
                        'message': 'Internal Server Error'
                    }
                }
            }
        }
    })    
    def get(self):
        try:
            current_user = get_jwt_identity()
            return {'message': f'Hello, User {current_user}!'}
        except Exception as e:
            return {'message': str(e)}, 500

        
class AdminOnlyResource(Resource):
    @jwt_required()
    @dynamic_role_required(can_read=True)
    @swag_from({
        'summary': 'Admin Only Resource',
        'description': 'Returns a message for admin users only. Requires a valid JWT token and admin role.',
        'responses': {
            200: {
                'description': 'Admin message',
                'examples': {
                    'application/json': {
                        'message': 'Hello, Admin!'
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
            },
            403: {
                'description': 'Forbidden: User does not have the required permission',
                'examples': {
                    'application/json': {
                        'msg': 'Read permission required'
                    }
                }
            }
        }
    })
    def get(self):
        return {'message': 'Hello, Admin!'}

class UserOnlyResource(Resource):
    @jwt_required()
    @dynamic_role_required(can_read=True)
    @swag_from({
        'summary': 'User Only Resource',
        'description': 'Returns a message for users only. Requires a valid JWT token and user role.',
        'responses': {
            200: {
                'description': 'User message',
                'examples': {
                    'application/json': {
                        'message': 'Hello, User!'
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
            },
            403: {
                'description': 'Forbidden: User does not have the required permission',
                'examples': {
                    'application/json': {
                        'msg': 'Read permission required'
                    }
                }
            }
        }
    })
    def get(self):
        return {'message': 'Hello, User!'}

class UpdateResource(Resource):
    @jwt_required()
    @dynamic_role_required(can_update=True)
    @swag_from({
        'summary': 'Update Resource',
        'description': 'Allows a user to update a resource. Requires a valid JWT token and update permission.',
        'responses': {
            200: {
                'description': 'Update successful',
                'examples': {
                    'application/json': {
                        'message': 'Update successful'
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
            },
            403: {
                'description': 'Forbidden: User does not have the required permission',
                'examples': {
                    'application/json': {
                        'msg': 'Update permission required'
                    }
                }
            }
        }
    })
    def put(self):
        return {'message': 'Update successful'}

class DeleteResource(Resource):
    @jwt_required()
    @dynamic_role_required(can_delete=True)
    @swag_from({
        'summary': 'Delete Resource',
        'description': 'Allows a user to delete a resource. Requires a valid JWT token and delete permission.',
        'responses': {
            200: {
                'description': 'Delete successful',
                'examples': {
                    'application/json': {
                        'message': 'Delete successful'
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
            },
            403: {
                'description': 'Forbidden: User does not have the required permission',
                'examples': {
                    'application/json': {
                        'msg': 'Delete permission required'
                    }
                }
            }
        }
    })
    def delete(self):
        return {'message': 'Delete successful'}

api_restful.add_resource(HelloWorld, '/hello')
api_restful.add_resource(TokenResource, '/token')
api_restful.add_resource(AdminOnlyResource, '/admin-only')
api_restful.add_resource(UserOnlyResource, '/user-only')
api_restful.add_resource(UpdateResource, '/update')
api_restful.add_resource(DeleteResource, '/delete')

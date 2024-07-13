from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify
from app.models import User, Permission

def dynamic_role_required(can_read=False, can_write=False, can_update=False, can_delete=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                current_user_id = get_jwt_identity()
                print(f"current_user_id: {current_user_id}")
                user = User.query.get(current_user_id)

                if user is None:
                    print("User not found")
                    return ({'message': 'User not found'}), 404

                path = request.path
                print(f"Checking permissions for user: {user.username}, path: {path}")
                permission = Permission.query.filter_by(user_id=user.id, endpoint=path).first()

                if permission is None:
                    print(f"Permission not found for user {user.username} on endpoint {path}")
                    return ({'message': 'Permission not found'}), 403

                if can_read and not permission.can_read:
                    print(f"Read permission required for user {user.username} on endpoint {path}")
                    return ({'message': 'Read permission required'}), 403
                if can_write and not permission.can_write:
                    print(f"Write permission required for user {user.username} on endpoint {path}")
                    return ({'message': 'Write permission required'}), 403
                if can_update and not permission.can_update:
                    print(f"Update permission required for user {user.username} on endpoint {path}")
                    return ({'message': 'Update permission required'}), 403
                if can_delete and not permission.can_delete:
                    print(f"Delete permission required for user {user.username} on endpoint {path}")
                    return ({'message': 'Delete permission required'}), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                print(f"Exception in dynamic_role_required: {str(e)}")
                return {'message': str(e)}
        return decorated_function
    return decorator

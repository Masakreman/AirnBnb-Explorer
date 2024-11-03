from flask import request, jsonify, make_response
import jwt
import globals
from functools import wraps

blacklist = globals.db.blacklist

# Enfore JWT token on routes
def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return make_response(jsonify({'error': 'Token is missing'}), 403)
        
        try:
            data = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
            # Store user data in request for further use
            request.user_data = data  
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'error': 'Token is expired, please log in again'}), 403)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'error': 'Token is invalid, Please log in again'}), 403)

        # Check if token is blacklisted
        bl_token = blacklist.find_one({"token": token})
        if bl_token is not None:
            return make_response(jsonify({'error': 'Token has been cancelled, Please log in again'}), 403)

        return func(*args, **kwargs)

    return jwt_required_wrapper

# Role-based access control decorator
def role_required(role):
    def check_role(func):
        @wraps(func)
        @jwt_required  # Ensure the token is present and valid
        def wrapper(*args, **kwargs):
            if 'role' not in request.user_data:
                return make_response(jsonify({'error': 'Role not found in token'}), 403)

            if request.user_data['role'] != role:
                return make_response(jsonify({'error': 'Access denied: insufficient permissions'}), 403)

            return func(*args, **kwargs)

        return wrapper
    return check_role

def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'error': 'Token not found, Please log in again'}), 403)
        try:
            data = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'error': 'Token is expired, please log in again'}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'error': 'Token is invalid, please log in again'}), 401)
        
        if data["admin"]:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify( {'error' : 'Admin access required' } ), 401 )
        
    return admin_required_wrapper
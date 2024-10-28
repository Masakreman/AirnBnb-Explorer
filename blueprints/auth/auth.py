from flask import Blueprint, request, jsonify, make_response
import bcrypt
import jwt
import datetime
import globals
from decorators import jwt_required


auth_bp = Blueprint('auth_bp', __name__)

users = globals.users
hosts = globals.hosts
blacklist = globals.blacklist

@auth_bp.route('/api/v1.0/login', methods=['GET'])
def login():
    auth = request.authorization

    if auth:
        # Check in users collection
        user = users.find_one({'user_name': auth.username})
        
        if user is not None:
            # Verify password for user
            if bcrypt.checkpw(auth.password.encode('utf-8'), user["password"]):
                token = jwt.encode({
                    'user': auth.username,
                    'role': 'user',
                    'admin': user['admin'],
                    'user_id': str(user['_id']),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }, globals.secret_key, algorithm="HS256")
                return make_response(jsonify({'token': token}), 200)
            else:
                return make_response(jsonify({'message': 'Bad password'}), 401)
        
        # Check in hosts collection if user not found in users
        host = hosts.find_one({'host_name': auth.username})

        if host is not None:
            # Verify password for host 
            if bcrypt.checkpw(auth.password.encode('utf-8'), host["password"]):
                token = jwt.encode({
                    'user': auth.username,
                    'role': 'host',
                    'admin': False,  # Assuming hosts are not admins
                    'host_id': str(host['_id']),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }, globals.secret_key, algorithm="HS256")
                return make_response(jsonify({'token': token}), 200)
        
        # If no user or host found
        return make_response(jsonify({'message': 'Bad username or password'}), 401)

    return make_response(jsonify({'message': 'Authentication required'}), 401)

@auth_bp.route('/api/v1.0/logout', methods=["GET"])
@jwt_required
def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token":token})
    return make_response(jsonify( {'message' : 'Logout successful' } ), 200 )
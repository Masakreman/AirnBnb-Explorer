from flask import Blueprint, request, jsonify, make_response
import bcrypt
import jwt
from datetime import datetime, timedelta
import globals
from decorators import jwt_required


auth_bp = Blueprint('auth_bp', __name__)

users = globals.users
hosts = globals.hosts
blacklist = globals.blacklist

@auth_bp.route('/api/v1.0/register/user', methods=['POST'])
def registerUser():

    # Check if a user with this name already exists
    if users.find_one({"user_name": request.form['user_name']}):
        return make_response(jsonify({"error": "user name already exists. Please choose a different name."}), 400)


    required_fields = [
        "user_name", "password"
    ]

    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in request.form]
    if missing_fields:
        return make_response(jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400)

    try:
        password = request.form['password'].encode('utf-8')
        hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())

        newUser = {
            "user_name": request.form['user_name'],
            "password": hashedPassword,
            "admin": False,
            "user_reviews": []
        }

        new_user = users.insert_one(newUser)
        new_user_link = "http://127.0.0.1:5000/api/v1.0/users/" \
        + str(new_user.inserted_id)
        return make_response(jsonify({"url" : new_user_link}), 201)
    except ValueError:
        return make_response(jsonify({"error": "Missing or invalid form data"}), 400)
    
@auth_bp.route('/api/v1.0/register/host', methods=['POST'])
def registerHost():
    # Check if a host with this name already exists
    if hosts.find_one({"host_name": request.form['host_name']}):
        return make_response(jsonify({"error": "Host name already exists. Please choose a different name."}), 400)

    required_fields = [
        "host_name", "password"
    ]

    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in request.form]
    if missing_fields:
        return make_response(jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400)

    try:
        password = request.form['password'].encode('utf-8')
        hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())

        newHost = {
            "host_name": request.form['host_name'],
            "host_verifications": [],
            "host_since": datetime.today().strftime('%Y-%m-%d'),
            "host_location": '',
            "host_about": '',
            "host_response_time": '',
            "host_response_rate": '',
            "host_acceptance_rate": '',
            "host_identity_verified": False,
            "current_listings": [],
            "password": hashedPassword,
            "admin": False,
        }

        new_host = hosts.insert_one(newHost)
        new_host_link = "http://127.0.0.1:5000/api/v1.0/hosts/" \
        + str(new_host.inserted_id)
        return make_response(jsonify({"url" : new_host_link}), 201)
    except ValueError:
        return make_response(jsonify({"error": "Missing or invalid form data"}), 400)

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
                    'exp': datetime.utcnow() + timedelta(minutes=30)
                }, globals.secret_key, algorithm="HS256")
                return make_response(jsonify({'token': token}), 200)
            else:
                return make_response(jsonify({'message': 'Bad username or password'}), 401)
        
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
                    'exp': datetime.utcnow() + timedelta(minutes=30)
                }, globals.secret_key, algorithm="HS256")
                return make_response(jsonify({'token': token}), 200)
        
        # If no user or host found
        return make_response(jsonify({'message': 'Bad username or password'}), 401)

    return make_response(jsonify({'message': 'Authentication required'}), 403)

@auth_bp.route('/api/v1.0/logout', methods=["GET"])
@jwt_required
def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token":token})
    return make_response(jsonify( {'message' : 'Logout successful' } ), 200 )
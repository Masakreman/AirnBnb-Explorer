from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
import globals
import jwt
from decorators import role_required, jwt_required, admin_required


users_bp = Blueprint('users_bp', __name__)

users = globals.users


@users_bp.route("/api/v1.0/users/<string:u_id>", methods=["GET"])
@admin_required
def show_one_user(u_id):
    user = users.find_one({'_id' : ObjectId(u_id)}, {"password": 0})

    if user is not None:
        user['_id'] = str(user['_id'])
        user['user_reviews'] = [str(review_id) for review_id in user['user_reviews']]

        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"error" : "Invalid listing ID"}), 404)
    
@users_bp.route("/api/v1.0/users", methods=["GET"])
@admin_required
def show_all_users():
    try:
        page_num, page_size = 1, 3
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        page_start = (page_size * (page_num - 1))

        if page_num < 1 or page_size < 1:
            return make_response(
                jsonify({"error": "Invalid pagination parameters"}), 400)

        data_to_return = []
        usersContainer = users.find({}, {"password": 0}).skip(page_start).limit(page_size)

        for user in usersContainer:
            user['_id'] = str(user['_id'])
            user['user_reviews'] = [str(review_id) for review_id in user['user_reviews']]
            data_to_return.append(user)

        return make_response(jsonify(data_to_return), 200)
    except Exception:
        return make_response(jsonify({"error": "An error occured retrieving users"}), 500)
    

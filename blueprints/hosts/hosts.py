from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
import globals
import jwt
from decorators import role_required, jwt_required, admin_required

hosts_bp = Blueprint('hosts_bp', __name__)

hosts = globals.hosts


@hosts_bp.route("/api/v1.0/hosts/<string:h_id>", methods=["GET"])
def show_one_host(h_id):
    host = hosts.find_one({'_id' : ObjectId(h_id)}, {"password": 0})

    if host is not None:
        host['_id'] = str(host['_id'])
        host['current_listings'] = [str(listing_id) for listing_id in host['current_listings']]
        return make_response(jsonify(host), 200)
    else:
        return make_response(jsonify({"error" : "Invalid listing ID"}), 404)
    
@hosts_bp.route("/api/v1.0/hosts", methods=["GET"])
def show_all_hosts():
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
        hostsContainer = hosts.find({}, {"password": 0}).skip(page_start).limit(page_size)

        for host in hostsContainer:
            host['_id'] = str(host['_id'])
            host['current_listings'] = [str(listing_id) for listing_id in host['current_listings']]
            data_to_return.append(host)

        return make_response(jsonify(data_to_return), 200)
    except Exception:
        return make_response(jsonify({"error": "An error occured retrieving hosts"}), 500)
    

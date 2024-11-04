from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
from datetime import datetime
import globals
from decorators import admin_required

operations_bp = Blueprint('operations_bp', __name__)

operations = globals.operations


@operations_bp.route("/api/v1.0/operations", methods=["GET"])
@admin_required
def show_all_operations():
    try:
        page_num, page_size = 1, 10
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        page_start = (page_size * (page_num - 1))

        if page_num < 1 or page_size < 1:
            return make_response(
                jsonify({"error": "Invalid pagination parameters"}), 400)
        

        data_to_return = []
        operationsContainer = operations.find({}).sort("dateOfOperation", -1).skip(page_start).limit(page_size)

        for operation in operationsContainer:
            operation['_id'] = str(operation['_id'])
            operation['entity_id'] = str(operation['entity_id'])
            operation['user_or_host_id'] = str(operation['user_or_host_id'])
            data_to_return.append(operation)

        return make_response(jsonify(data_to_return), 200)
    except Exception:
        return make_response(jsonify({"error": "An error occured retrieving operations"}), 500)
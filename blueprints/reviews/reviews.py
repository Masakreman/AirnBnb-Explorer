from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
import globals
from decorators import role_required, jwt_required, admin_required

reviews_bp = Blueprint('reviews_bp', __name__)

listings = globals.listings

@reviews_bp.route("/api/v1.0/listings/<string:id>/reviews", methods=["GET"])
def show_all_reviews(id):
    data_to_return = []

    page_num, page_size = 1, 3
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    listing = listings.find_one({"_id" : ObjectId(id)}, {"reviews" : 1, "_id" : 0 })
    if not listing:
        return make_response(jsonify({"error": "Listing not found"}), 404)
    
    reviews = listing.get("reviews", [])[page_start:page_start + page_size]

    for review in reviews:
        review['_id'] = str(review['_id']),
        review['user_id'] = str(review['user_id'])
        data_to_return.append(review)

    return make_response(jsonify(data_to_return), 200)
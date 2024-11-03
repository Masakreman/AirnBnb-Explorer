from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
from datetime import datetime
import globals
import jwt
from decorators import role_required, jwt_required, admin_required

reviews_bp = Blueprint('reviews_bp', __name__)

listings = globals.listings
users = globals.users

@reviews_bp.route("/api/v1.0/listings/<string:id>/reviews", methods=["GET"])
def show_all_reviews(id):
    data_to_return = []

    page_num, page_size = 1, 3
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    if page_num < 1 or page_size < 1:
            return make_response(
                jsonify({"error": "Invalid pagination parameters"}), 400)

    listing = listings.find_one({"_id" : ObjectId(id)}, {"reviews" : 1, "_id" : 0 })
    if not listing:
        return make_response(jsonify({"error": "Listing not found"}), 404)
    
    reviews = listing.get("reviews", [])[page_start:page_start + page_size]

    for review in reviews:
        review['_id'] = str(review['_id']),
        review['user_id'] = str(review['user_id'])
        data_to_return.append(review)

    return make_response(jsonify(data_to_return), 200)

@reviews_bp.route('/api/v1.0/listings/<string:l_id>/reviews', methods=['POST'])
@role_required('user')
@jwt_required
def create_review(l_id):

    required_fields = [
        "comments"
    ]

    # Decode the token to get the host_id
    token = request.headers.get('x-access-token')
    decoded = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
    user_id = decoded['user_id']

    # Get users info
    user_info = users.find_one({"_id" : ObjectId(user_id)})
    if not user_info:
        return make_response(jsonify({"error": "User not found"}), 404)
    user_name = user_info.get("user_name")
    
    # Check if missing required fields
    missing_fields = [field for field in required_fields if field not in request.form]
    if missing_fields:
        return make_response(jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400)
    
    # Check if comments field empty
    comments = request.form.get("comments", "").strip()
    if not comments:
        return make_response(jsonify({"error": "Comments field cannot be empty"}), 400)
    
    try:
        review_id = ObjectId()  # Create the review ID first
        new_review = {
            "_id": review_id,
            "user_id": ObjectId(user_id),
            "user_name": user_name,
            "comments": request.form["comments"],
            "date": datetime.today().strftime('%Y-%m-%d')
        }

        # Updating the target listing to add the new_review 
        result = listings.update_one({ "_id" : ObjectId(l_id)}, { "$push" : {"reviews" : new_review }})

        if result.matched_count == 0:
            return make_response(jsonify({"error": "Listing not found"}), 404)
        
        # Add _id of the review to the users collection user_reviews array
        user_result = users.update_one({"_id": ObjectId(user_id)}, {"$push": {"user_reviews": review_id}})

        if user_result.modified_count == 0:
            # If user update failed, you might want to roll back the listing update
            listings.update_one(
                {"_id": ObjectId(l_id)},
                {"$pull": {"reviews": {"_id": review_id}}}
            )
            return make_response(jsonify({"error": "Failed to update user reviews"}), 500)
        
        new_review_link = f"http://127.0.0.1:5000/api/v1.0/listings/{l_id}/reviews/{new_review['_id']}"
        return make_response(jsonify({"url" : new_review_link}), 201)

    except (ValueError, TypeError):
        return make_response(jsonify({"error": "Invalid form data"}), 400)
    

@reviews_bp.route("/api/v1.0/listings/<string:l_id>/reviews/<string:r_id>", methods=["PUT"])
@role_required('user')
def edit_review(l_id, r_id):

    # Decode the token to get the user_id
    token = request.headers.get('x-access-token')
    decoded = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
    user_id = decoded['user_id']

    # Find the listing with the given review
    listing = listings.find_one({"_id": ObjectId(l_id), "reviews._id": ObjectId(r_id)}, {"reviews.$": 1})
    
    if not listing or not listing.get("reviews"):
        return make_response(jsonify({"error": "Review not found"}), 404)
    
    review = listing["reviews"][0]

    # validate if the user is the owner of the review
    if str(review["user_id"]) != user_id:
        return make_response(jsonify({"Permission Denied": "User can only edit reviews belonging to them"}), 403)

    # Update the review's comment
    edited_review = {
        "reviews.$.comments": request.form['comments']
    }
    result = listings.update_one(
        {"_id": ObjectId(l_id), "reviews._id": ObjectId(r_id)},
        {"$set": edited_review}
    )

    if result.matched_count == 0:
        return make_response(jsonify({"error": "Failed to update review"}), 500)

    # Return the URL of the edited review
    edited_review_url = f"http://127.0.0.1:5000/api/v1.0/listings/{l_id}/reviews/{r_id}"
    return make_response(jsonify({"url": edited_review_url}), 200)

@reviews_bp.route("/api/v1.0/listings/<string:l_id>/reviews/<string:r_id>", methods=["GET"])
def show_one_review(l_id, r_id):
    # Retrieve the review to get the user_id
    review = listings.find_one(
        {"_id": ObjectId(l_id), "reviews._id": ObjectId(r_id)},
        {"reviews.$": 1}  # This only retrieves the matched review
    )
    
    # Check if the review exists
    if not review or "reviews" not in review or not review["reviews"]:
        return make_response(jsonify({"error": "Review not found"}), 404)
    
    # Get data from the first matched review in array
    review_data = review["reviews"][0]
    
    # Convert the Object id's to string to be abelt to return
    review_data['_id'] = str(review_data['_id'])
    review_data['user_id'] = str(review_data['user_id'])

    return make_response(jsonify(review_data), 200)  # Return the review data with a 200 status code

@reviews_bp.route("/api/v1.0/listings/<string:l_id>/reviews/<string:r_id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_review(l_id, r_id):
    # Retrieve the review to get the user_id
    review = listings.find_one(
        {"_id": ObjectId(l_id), "reviews._id": ObjectId(r_id)},
        {"reviews.$": 1}
    )

    # Check if the review exists
    if not review or "reviews" not in review:
        return make_response(jsonify({"error": "Review not found"}), 404)

    # Get the user_id from the review
    user_id = review["reviews"][0]["user_id"]

    # Remove the review from the listing's reviews array
    listings.update_one(
        {"_id": ObjectId(l_id)},
        {"$pull": {"reviews": {"_id": ObjectId(r_id)}}}
    )

    # Remove the review ID from the user's user_reviews array
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"user_reviews": ObjectId(r_id)}}
    )

    return make_response(jsonify({}), 204)


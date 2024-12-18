from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
from datetime import datetime
import globals
import jwt
from decorators import role_required, jwt_required, admin_required

reviews_bp = Blueprint('reviews_bp', __name__)

listings = globals.listings
users = globals.users
operations = globals.operations
log_operation = globals.log_operation

def convert_object_ids(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: convert_object_ids(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_object_ids(item) for item in obj]
    return obj

@reviews_bp.route('/api/v1.0/listings/<string:l_id>/reviews', methods=['GET'])
def show_all_reviews(l_id):
    try:
        # Find the listing
        listing = listings.find_one({"_id": ObjectId(l_id)})
        if not listing:
            return make_response(jsonify({"error": "Listing not found"}), 404)
        
        # Get reviews from the listing and convert all ObjectIds
        reviews = listing.get('reviews', [])
        processed_reviews = convert_object_ids(reviews)
        
        return make_response(jsonify(processed_reviews), 200)
        
    except Exception as e:
        print(f"Error fetching reviews: {str(e)}")
        return make_response(jsonify({"error": str(e)}), 500)

@reviews_bp.route('/api/v1.0/listings/<string:l_id>/reviews', methods=['POST'])
def create_review(l_id):
    try:
        # First verify the listing exists
        listing = listings.find_one({"_id": ObjectId(l_id)})
        if not listing:
            return make_response(jsonify({"error": "Listing not found"}), 404)

        # Create new review without _id field since it's embedded
        new_review = {
            "user_name": request.form["user_name"],
            "comments": request.form["comments"],
            "date": request.form.get("date", datetime.today().strftime('%Y-%m-%d')),
            "_id": ObjectId()  # Add a unique ID for each review
        }

        # Update the listing with the new review
        result = listings.update_one(
            {"_id": ObjectId(l_id)}, 
            {"$push": {"reviews": new_review}}
        )

        if result.matched_count == 0:
            return make_response(jsonify({"error": "Listing not found"}), 404)
        
        if result.modified_count == 0:
            return make_response(jsonify({"error": "Review was not added"}), 500)

        # Convert ObjectIds before returning
        processed_review = convert_object_ids(new_review)
        return make_response(jsonify(processed_review), 201)

    except Exception as e:
        print(f"Error creating review: {str(e)}")
        return make_response(jsonify({"error": str(e)}), 500)
    
@reviews_bp.route("/api/v1.0/listings/<string:l_id>/reviews/<string:r_id>", methods=["PUT"])
@role_required('user')
def edit_review(l_id, r_id):

    # Decode the token to get the user_id
    token = request.headers.get('x-access-token')
    decoded = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
    role = decoded['role']
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

    # After adding a new review
    log_operation("edit_review", r_id, user_id, role)

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
    token = request.headers.get('x-access-token')
    decoded = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
    admin_id = decoded['user_id']

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

    # After deleting a review
    log_operation("delete_review", r_id, admin_id, "admin")

    return make_response(jsonify({}), 204)


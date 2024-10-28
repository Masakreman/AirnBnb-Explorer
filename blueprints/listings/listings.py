from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
import random
import globals
import jwt
from decorators import role_required

listings_bp = Blueprint('listings_bp', __name__)

listings = globals.listings
hosts = globals.hosts
neighbourhoods = globals.neighbourhoods
geodata = globals.geodata

@listings_bp.route("/api/v1.0/listings", methods=["GET"])
def show_all_listings():
    page_num, page_size = 1, 3
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    data_to_return = []
    for listing in listings.find().skip(page_start).limit(page_size):
        listing['_id'] = str(listing['_id'])
        
        # Convert the host _id and each _id in current_listings to strings
        if 'host' in listing and isinstance(listing['host'], dict):
            listing['host']['_id'] = str(listing['host']['_id'])
            if 'current_listings' in listing['host']:
                listing['host']['current_listings'] = [str(listing_id) for listing_id in listing['host']['current_listings']]
        
        # Convert review _id fields and user_id fields in reviews to strings
        if 'reviews' in listing:
            for review in listing['reviews']:
                review['_id'] = str(review['_id'])
                review['user_id'] = str(review['user_id'])
        
        data_to_return.append(listing)

    return make_response(jsonify(data_to_return), 200)

@listings_bp.route("/api/v1.0/listings/<string:id>", methods=["GET"])
def show_one_listing(id):
    listing = listings.find_one({'_id' : ObjectId(id)})

    if listing is not None:
        listing['_id'] = str(listing['_id'])

        # Convert the host _id and each _id in current_listings to strings
        if 'host' in listing:
            if '_id' in listing['host']:
                listing['host']['_id'] = str(listing['host']['_id'])
                if 'current_listings' in listing['host']:
                    listing['host']['current_listings'] = [str(listing_id) for listing_id in listing['host']['current_listings']]
        
        # Convert review _id fields and user_id fields in reviews to strings
        if 'reviews' in listing:
            if '_id' in listing['reviews']:
                for review in listing['reviews']:
                    review['_id'] = str(review['_id'])
                    review['user_id'] = str(review['user_id'])
        
        return make_response(jsonify(listing), 200)
    else:
        return make_response(jsonify({"error" : "Invalid listing ID"}))
    



@listings_bp.route('/api/v1.0/listings', methods=['POST'])
@role_required('host')
def create_listing():
    host_info = {}
    required_fields = [
        "name", "property_type", "room_type",
        "accomodates", "bathrooms", "bedrooms",
        "beds", "price", "minimum_nights"
    ]


    token = request.headers.get('x-access-token')
    # Decode the token to get the host_id
    decoded = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
    host_id = decoded['host_id']

    host_info = hosts.find_one({'_id' : ObjectId(host_id)})
    if host_info:
        host_info = {
                "_id": str(host_info['_id']),  # Convert ObjectId to string
                "host_name": host_info.get("host_name"),
                "host_verifications": host_info.get("host_verifications"),
                "host_since": host_info.get("host_since"),
                "host_location": host_info.get("host_location"),
                "host_about": host_info.get("host_about"),
                "host_response_time": host_info.get("host_response_time"),
                "host_response_rate": host_info.get("host_response_rate"),
                "host_acceptance_rate": host_info.get("host_acceptance_rate"),
                "host_identity_verified": host_info.get("host_identity_verified")
            }

    # Select a random neighbourhood
        neighbourhood = neighbourhoods.aggregate([{"$sample": {"size": 1}}]).next()
        selected_neighbourhood_name = neighbourhood["neighbourhood_name"]
        boundary = neighbourhood["boundary_coordinates"]
        
        # Generate random coordinates within the neighbourhood's boundary
        rand_lat = boundary["latitude_min"] + (boundary["latitude_max"] - boundary["latitude_min"]) * random.random()
        rand_lng = boundary["longitude_min"] + (boundary["longitude_max"] - boundary["longitude_min"]) * random.random()

        # Format location as GeoJSON Point
        random_coordinates = {
            "type": "Point",
            "coordinates": [rand_lng, rand_lat]  # Longitude first, then latitude
        }
    
    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in request.form]
    if missing_fields:
        return make_response(jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400)
    
    try:
        new_listing = {
            "listing_url": "",
            "picture_url": "",
            "name": request.form["name"],
            "description": "",
            "property_type": request.form["property_type"],
            "room_type": request.form["room_type"],
            "accomodates": request.form["accomodates"],
            "bathrooms": request.form["bathrooms"],
            "bedrooms": request.form["bedrooms"],
            "beds": request.form["beds"],
            "amenities": [],
            "price": request.form["price"],
            "minimum_nights": request.form["minimum_nights"],
            "maximum_nights": "",
            "number_of_reviews": "",
            "review_scores_rating": "",
            "review_scores_location": "",
            "host": host_info,
            "location": random_coordinates,
            "neighbourhood": selected_neighbourhood_name,
            "reviews": []
        }

        new_listing_id = listings.insert_one(new_listing)
        new_listing_link = "http://127.0.0.1:5000/api/v1.0/listings/" \
        + str(new_listing_id.inserted_id)
        return make_response(jsonify({"url" : new_listing_link}), 201)
    except ValueError:
        return make_response(jsonify({"error" : "Missing or invalud form data"}), 400)




    # if "name" in request.form and "town" in request.form and "rating" in request.form:
    #     try:
    #         if int(request.form["rating"]) <= 5 and int(request.form["rating"]) >= 1:
    #             new_business = {
    #                 "name": request.form["name"],
    #                 "town": request.form["town"],
    #                 "rating": request.form["rating"],
    #                 "reviews": []
    #             }
    #             new_business_id = businesses.insert_one(new_business)
    #             new_business_link = "http://127.0.0.1:5000/api/v1.0/businesses/" \
    #                 + str(new_business_id.inserted_id)
    #             return make_response(jsonify({"url" : new_business_link}), 201)
    #         else:
    #             return make_response(jsonify({"error" : "Rating must be between 1 - 5"}), 400)
    #     except ValueError:
    #         return make_response(jsonify({"error" : "Missing or invalid form data. Rating must be between 1 - 5"}), 400)
    # return make_response(jsonify({"error": "Missing required form data"}), 400)

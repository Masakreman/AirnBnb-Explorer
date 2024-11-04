from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
import random
import globals
import jwt
from decorators import role_required, jwt_required, admin_required

listings_bp = Blueprint('listings_bp', __name__)

listings = globals.listings
hosts = globals.hosts
neighbourhoods = globals.neighbourhoods
operations = globals.operations
log_operation = globals.log_operation

@listings_bp.route("/api/v1.0/listings", methods=["GET"])
def show_all_listings():
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
        
        query = {}

        # match specific params
        if 'neighbourhood' in request.args:
            query['neighbourhood'] = request.args['neighbourhood']
        
        if 'room_type' in request.args:
            query['room_type'] = request.args['room_type']

        # Numeric greater than or equal queries
        numeric_gte_fields = {
            'accommodates': 'accommodates',
            'bathrooms': 'bathrooms',
            'bedrooms': 'bedrooms',
            'rating_min': 'review_scores_rating'
        }

        for param, field in numeric_gte_fields.items():
            if param in request.args:
                query[field] = {'$gte': float(request.args[param])}

        # Handle ratings 
        if 'rating_max' in request.args:
            if 'review_scores_rating' in query:
                query['review_scores_rating']['$lte'] = float(request.args['rating_max'])
            else:
                query['review_scores_rating'] = {'$lte': float(request.args['rating_max'])}

        # Handle price ranges
        price_conditions = []
        if 'price_min' in request.args:
            price_conditions.append({'price': {'$gte': float(request.args['price_min'])}})
        if 'price_max' in request.args:
            price_conditions.append({'price': {'$lte': float(request.args['price_max'])}})
        
        # Check how many price conditions are given if 1 add it to query if 2 then combine conditions that the listing must match
        if price_conditions:
            if len(price_conditions) == 1:
                query.update(price_conditions[0])
            else:
                query['$and'] = price_conditions

        # Execute query with pagination
        data_to_return = []
        for listing in listings.find(query).skip(page_start).limit(page_size):
            listing['_id'] = str(listing['_id'])
            
            # Convert the host _id to a string
            if 'host' in listing and isinstance(listing['host'], dict):
                listing['host']['_id'] = str(listing['host']['_id'])
            
            # Convert review _id fields and user_id fields in reviews to strings
            if 'reviews' in listing:
                for review in listing['reviews']:
                    review['_id'] = str(review['_id'])
                    review['user_id'] = str(review['user_id'])
            
            data_to_return.append(listing)

        return make_response(jsonify(data_to_return), 200)
    except Exception:
        return make_response(jsonify({"error": "An error occurred getting listings"}), 500)

@listings_bp.route("/api/v1.0/listings/<string:id>", methods=["GET"])
def show_one_listing(id):
    listing = listings.find_one({'_id' : ObjectId(id)})

    if not listing:
        return make_response(jsonify({"error": "Listing not found"}), 404)

    if listing is not None:
        listing['_id'] = str(listing['_id'])

        # Convert the host _id to string
        if 'host' in listing:
            if '_id' in listing['host']:
                listing['host']['_id'] = str(listing['host']['_id'])
        
        # Convert review _id fields and user_id fields in reviews to strings
        if 'reviews' in listing:
            for review in listing['reviews']:
                review['_id'] = str(review['_id'])
                review['user_id'] = str(review['user_id'])
        
        return make_response(jsonify(listing), 200)
    else:
        return make_response(jsonify({"error" : "Invalid listing ID"}))
    
@listings_bp.route('/api/v1.0/listings', methods=['POST'])
@role_required('host')
def create_listing():
    # When a host creates a listing need to add it to their current_listings in host collection, also remove after removing a listing

    host_info = {}

    required_fields = [
        "name", "property_type", "room_type",
        "accomodates", "bathrooms", "bedrooms",
        "beds", "price", "minimum_nights"
    ]

    # Decode the token to get the host_id and from that get the hosts record
    token = request.headers.get('x-access-token')
    decoded = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
    host_id = decoded['host_id']
    role = decoded['role']
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
        price = float(request.form["price"])  # Attempt to convert price to a float
    except ValueError:
        return make_response(jsonify({"error": "Invalid data type"}), 400)
    
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

        id = new_listing_id.inserted_id

        # Add the listing ID to the host's current_listings
        hosts.update_one(
            {"_id": ObjectId(host_id)},
            {"$push": {"current_listings": new_listing_id.inserted_id}}  # Use the inserted_id here
        )

        # After adding a new listing
        log_operation("create_listing", id, host_id, role)

        new_listing_link = "http://127.0.0.1:5000/api/v1.0/listings/" \
        + str(new_listing_id.inserted_id)
        return make_response(jsonify({"url" : new_listing_link}), 201)
    except ValueError:
        return make_response(jsonify({"error" : "Missing or invalud form data"}), 400)

@listings_bp.route("/api/v1.0/listings/<string:id>", methods=["PUT"])
@role_required('host')
def edit_listing(id):
    fields_in_listing = [
        "listing_url", "picture_url", "name", "description", "property_type", "room_type",
        "accomodates", "bathrooms", "bedrooms", "beds", "amenities", "price", "minimum_nights", "maximum_nights", "number_of_reviews",
        "review_scores_rating", "review_scores_location", "location", "neighbourhood"
    ]

    # Decode the token to get the host_id and from that get the hosts record
    token = request.headers.get('x-access-token')
    decoded = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
    role = decoded['role']
    host_id = decoded['host_id']

    # Retrieve the listing from the database
    listing = listings.find_one({"_id": ObjectId(id)})
    if not listing:
        return make_response(jsonify({"error": "Listing not found"}), 404)


     # validate if the user is the owner of the review
    if str(listing["host"]["_id"]) != host_id:
        return make_response(jsonify({"Permission Denied": "User can only edit reviews belonging to them"}), 403)
    
    update_fields = {}
    for field in fields_in_listing:
        if field in request.form:
            if field == "amenities":
                # Split amenities by comma, trim whitespace, and handle it as a list
                update_fields[field] = [amenity.strip() for amenity in request.form[field].split(',')]
            else:
                update_fields[field] = request.form[field]

    # Update the listing
    result = listings.update_one({'_id': ObjectId(id)}, {"$set": update_fields})

    if result.matched_count == 1:

        # After editing a listing
        log_operation("edit_listing", id, host_id, role)

        edited_listing_link = "http://127.0.0.1:5000/api/v1.0/listings/" + id
        return make_response(jsonify({"url" : edited_listing_link}), 200)
    else:
        return make_response(jsonify({"error" : "Invalid Listing id"}))
    
@listings_bp.route("/api/v1.0/listings/<string:id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_listing(id):
    token = request.headers.get('x-access-token')
    decoded = jwt.decode(token, globals.secret_key, algorithms=["HS256"])
    admin_id = decoded['user_id']

    # First, find the listing to retrieve the host_id
    listing = listings.find_one({"_id": ObjectId(id)})
    if listing is None:
        return make_response(jsonify({"Error": "Listing not found"}), 404)

    # Now that we have the listing, we can get the host_id
    host_id = listing["host"]["_id"]

    # Now delete the listing
    result = listings.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 1:
        # Remove the listing from the host's current_listings
        hosts.update_one({"_id": ObjectId(host_id)}, {"$pull": {"current_listings": ObjectId(id)}})

        # deleting a listing
        log_operation("delete_listing", id, admin_id, "admin")
        
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"Error": "Failed to delete listing"}), 500)

@listings_bp.route("/api/v1.0/listings/totalPages", methods=["GET"])
def total_pages():
    page_num, page_size = 1, 3
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))

    if page_num < 1 or page_size < 1:
        return make_response(
            jsonify({"error": "Invalid pagination parameters"}), 400)
    
    total_listings = listings.count_documents({})

    total_pages = (total_listings + page_size - 1) // page_size

    response = {
        "Listings per Page": page_size,
        "Current Page": page_num,
        "Total pages Needed": total_pages,
        "Total listings": total_listings
    }

    return make_response(jsonify(response), 200)

@listings_bp.route("/api/v1.0/listings/priceRangeSummary", methods=["GET"])
def price_range_summary():
    try:
        price_ranges = [
            {"min": 0, "max": 50, "label": "$0-$50"},
            {"min": 50, "max": 100, "label": "$50-$100"},
            {"min": 100, "max": 150, "label": "$100-$150"},
            {"min": 150, "max": 200, "label": "$150-$200"},
            {"min": 200, "max": 300, "label": "$200-$300"},
            {"min": 300, "max": 500, "label": "$300-$500"},
            {"min": 500, "max": 1000, "label": "$500-$1000"},
        ]

        # Create boundaries list
        boundaries = [range["min"] for range in price_ranges] # Get each min value from price ranges
        boundaries.append(price_ranges[-1]["max"])  # Upper Boundary

        pipeline = [
            {
                "$addFields": {
                    "price_as_number": {
                        "$convert": {
                            "input": "$price",
                            "to": "decimal",
                            "onError": None,  # Error handling for conversion to decimal value
                            "onNull": None
                        }
                    }
                }
            },
            {
                "$match": {
                    "price_as_number": {"$ne": None}  # Filter out any invalid Prices (there shouldnt be any but just in case)
                }
            },
            {
                # using the a bucket to group documents by $price_as_number which is decimal price
                "$bucket": {
                    "groupBy": "$price_as_number",
                    "boundaries": boundaries,
                    "default": "Over $1000", # Values that dont fit into boundaries are classed by 1000+ by default
                    "output": {
                        "count": {"$sum": 1}, # Get number of docs in each bucket i.e in each boundary
                        "listings": {
                            "$push": { # store basic information for each listing
                                "id": "$_id",
                                "name": "$name",
                                "price": "$price"
                            }
                        }
                    }
                }
            }
        ]

        # Run the aggregation pipeline
        result = list(listings.aggregate(pipeline))

        # Format the response with corresponding labels and additional info
        formatted_response = []

        # iterate over each item in the pipeline output (result) 
        # Each range_data corresponds to a bucket created in agrregation pipeline i.e couts of listings in each price range
        for i, range_data in enumerate(result):
            if isinstance(range_data["_id"], str):  # Handle over 1000 cases 
                range_info = {
                    "range": range_data["_id"],
                    "min": 1000,
                    "max": None,
                }
            else:
                range_info = { # Range dictionary to store all other price range buckets
                    "range": price_ranges[i]["label"],
                    "min": price_ranges[i]["min"],
                    "max": price_ranges[i]["max"],
                }

            # Convert ObjectId to string for each listing in the current range
            listings_with_string_ids = []
            for listing in range_data["listings"]:
                listing["id"] = str(listing["id"])  # Convert ObjectId to string
                listings_with_string_ids.append(listing)
            
            formatted_response.append({ # for each price range we have a new dictionary
                **range_info, # get contents of range_info using unpacking operator ** to get its key-value pairs
                "count": range_data["count"], # count listings in this price range
                "percentage": round((range_data["count"] / listings.count_documents({})) * 100, 2), # Calculate a percentage value of listings in this range vs Overall to 2 decimal palces
                "listings": listings_with_string_ids # Array of detailed listing information i.e _id, name, price
            })

        return make_response(jsonify({"data": formatted_response, "total_listings": listings.count_documents({})}), 200)

    except Exception:
        return make_response(jsonify({"error": "An error Occurred "}), 500)
    
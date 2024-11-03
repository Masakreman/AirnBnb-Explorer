from flask import request, jsonify, make_response, Blueprint
from bson import ObjectId
import globals

locations_bp = Blueprint('locations_bp', __name__)

listings = globals.listings
wifiLocations = globals.wifiLocations

@locations_bp.route("/api/v1.0/listings/<string:l_id>/wifi", methods=["GET"])
def get_nearest_wifi(l_id):
    page_num, page_size = 1, 5
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))

    if page_num < 1 or page_size < 1:
        return make_response(
            jsonify({"error": "Invalid pagination parameters"}), 400)
    
    # Fetch the listing based on the listing id 
    listing = listings.find_one({"_id": ObjectId(l_id)})
    if not listing:
        return make_response(jsonify({"error": "Listing not found"}), 404)

    location = listing.get("location")
    if not location:
        return make_response(jsonify({"error": "This listing doesn't contain a location"}), 400)

    # Get queryString parameters for filtering
    indoor_outdoor_filter = request.args.get("setting")
    max_distance_km = int(request.args.get("maxDistance", 50))
    max_distance = max_distance_km * 1000

    # Build the aggregation pipeline
    pipeline = [
        {
            "$geoNear": {
                "near": {
                    "type": "Point",
                    "coordinates": location["coordinates"]
                },
                "maxDistance": max_distance,
                "distanceField": "distance",
                "spherical": True
            }
        },
        {
            "$project": {
                "properties": 1,
                "geometry": 1,
                "distance": 1
            }
        }
    ]

    # optional filter for matching by Indoor/outddor parameters
    match_stage = {}
    if indoor_outdoor_filter:
        match_stage["properties.Indoor/Outdoor"] = indoor_outdoor_filter.capitalize()

    # use $match only if queryString provided
    if match_stage:
        pipeline.append({"$match": match_stage})

   # Sort by closest
    pipeline.append({"$sort": {"distance": 1}})

    # Skip and limit for pagination
    pipeline.append({"$skip": page_size * (page_num - 1)})  # Skip previous pages
    pipeline.append({"$limit": page_size})  # Limit to the page size

    # Run the aggregate pipeline
    nearby_wifi = wifiLocations.aggregate(pipeline)
    nearby_wifi_list = list(nearby_wifi)

    # formatting _id to string and distance in km
    for wifi in nearby_wifi_list:
        wifi['_id'] = str(wifi['_id'])
        wifi['distance_km'] = round(wifi['distance'] / 1000, 2)

    if nearby_wifi_list:
        return make_response(jsonify(nearby_wifi_list), 200)
    else:
        return make_response(jsonify({"error": "No nearby Wi-Fi locations found"}), 404)

from pymongo import MongoClient
import random

# Define neighborhoods with bounding box coordinates (southwest and northeast corners)
locations = {
    "Temple Bar": [53.3441, -6.2675, 53.3460, -6.2620],
    "Ranelagh": [53.3244, -6.2582, 53.3284, -6.2477],
    "Ballsbridge": [53.3315, -6.2333, 53.3387, -6.2222],
    "Clontarf": [53.3621, -6.1938, 53.3703, -6.1782],
    "Phibsborough": [53.3567, -6.2806, 53.3623, -6.2734],
    "Dublin Docklands": [53.3467, -6.2477, 53.3529, -6.2312],
    "Smithfield": [53.3485, -6.2838, 53.3530, -6.2782],
    "Stoneybatter": [53.3517, -6.2818, 53.3561, -6.2730],
    "Sandymount": [53.3298, -6.2224, 53.3372, -6.2081],
    "Donnybrook": [53.3242, -6.2403, 53.3308, -6.2251],
    "Rathmines": [53.3241, -6.2634, 53.3290, -6.2483],
    "Drumcondra": [53.3684, -6.2585, 53.3721, -6.2482],
    "Portobello": [53.3316, -6.2682, 53.3354, -6.2611],
    "Blackrock": [53.3009, -6.1838, 53.3085, -6.1668],
    "Inchicore": [53.3380, -6.3354, 53.3432, -6.3258],
    "Terenure": [53.3078, -6.2925, 53.3137, -6.2805],
    "Cabra": [53.3643, -6.2878, 53.3702, -6.2768],
    "Raheny": [53.3821, -6.1798, 53.3891, -6.1591],
    "Chapelizod": [53.3474, -6.3447, 53.3531, -6.3368]
}

# Connect to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.airbnb
listings = db.listings

# Update listings with a random neighborhood and random location coordinates
for listing in listings.find():
    # Choose a random neighborhood and get its bounding box
    neighborhood_name, bounds = random.choice(list(locations.items()))
    min_lat, min_lon, max_lat, max_lon = bounds
    
    # Generate random coordinates within the bounding box
    rand_lat = min_lat + (max_lat - min_lat) * random.random()
    rand_lon = min_lon + (max_lon - min_lon) * random.random()
    
    # Update listing with neighborhood and location fields
    listings.update_one(
        { "_id": listing["_id"] },
        { "$set": {
                "neighbourhood": neighborhood_name,
                "location": {
                    "type": "Point",
                    "coordinates": [rand_lon, rand_lat]
                }
            }
        }
    )

print("Listings updated with random neighborhoods and locations.")

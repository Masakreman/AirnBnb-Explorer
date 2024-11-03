from pymongo import MongoClient
from bson import ObjectId

# Setup MongoDB client and database
client = MongoClient("mongodb://localhost:27017/")
db = client['airbnb']
listings = db.listings
users = db.users

# Get all users
all_users = users.find()

for user in all_users:
    user_id = user['_id']
    # Find all reviews by this user in the listings collection
    user_reviews_ids = []
    listings_with_user_reviews = listings.find({"reviews.user_id": user_id})
    
    for listing in listings_with_user_reviews:
        for review in listing.get("reviews", []):
            if review["user_id"] == user_id:
                user_reviews_ids.append(review["_id"])

    # Update the user document with the collected review IDs
    users.update_one(
        {"_id": user_id},
        {"$set": {"user_reviews": user_reviews_ids}}
    )

print("User reviews arrays have been updated successfully.")

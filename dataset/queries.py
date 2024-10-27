from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.airbnb

# Remove current_listings field from all documents with an empty current_listings array
result = db.listings.update_many(
    { "current_listings": { "$exists": True, "$eq": [] } },  # Match documents where current_listings is an empty array
    { "$unset": { "current_listings": "" } }  # Remove current_listings field
)

# Print the number of documents updated
print(f'Documents updated: {result.modified_count}')

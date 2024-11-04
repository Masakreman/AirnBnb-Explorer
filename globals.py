from pymongo import MongoClient
import secrets
from datetime import datetime
from bson import ObjectId


client = MongoClient("mongodb://127.0.0.1:27017")
db = client.airbnb
listings = db.listings
users = db.users
hosts = db.hosts
neighbourhoods = db.neighbourhoods
blacklist = db.blacklist
wifiLocations = db.wifi_locations
operations = db.operations

secret_key = secrets.token_hex(16)

def log_operation(operation, entity_id, user_or_host_id, role):
    try:
        # Add error handling for ObjectId conversion
        entity_id_obj = ObjectId(entity_id) if isinstance(entity_id, str) else entity_id
        user_host_id_obj = ObjectId(user_or_host_id) if isinstance(user_or_host_id, str) else user_or_host_id

        operations.insert_one({
            "operation": operation,
            "entity_id": entity_id_obj,
            "user_or_host_id": user_host_id_obj,
            "role": role,
            "dateOfOperation": datetime.utcnow()
        })
        print(f"Operation logged successfully: {operation} by {role}")
    except Exception as e:
        print(f"Error in log_operation: {str(e)}")
        raise  # Re-raise the exception for the caller to handle


from pymongo import MongoClient
import secrets


client = MongoClient("mongodb://127.0.0.1:27017")
db = client.airbnb
listings = db.listings
users = db.users
hosts = db.hosts
neighbourhoods = db.neighbourhoods
blacklist = db.blacklist

secret_key = secrets.token_hex(16)
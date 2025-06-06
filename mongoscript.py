from pymongo import MongoClient
import datetime

username = "gauravgondane1"
password = "oi5B2tXIG4kKRqUM"

client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.khnkpqj.mongodb.net/")

db = client.scrapy
posts = db.test_collection

doc = post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc)
}

post_id = posts.insert_one(post).inserted_id
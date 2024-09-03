#!/usr/bin/env python3
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
import os
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime

uri = os.environ["MONGODB_URI"]
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

for db_info in client.list_database_names():
    print(db_info)
db = client["finances"]
spending = db["spending"]

try:
    spending.drop()
except pymongo.errors.OperationFailure:
    print(
        "An authentication error was received. Are your username and password correct in your connection string?"
    )
    sys.exit(1)

spending.insert_one(
    {
        "date": datetime(2024, 9, 1),
        "amount": 58.13,
        "category": "furniture",
        "vendor": "Amazon",
        "item": "desk",
        "recurring": False,
    }
)

for doc in spending.find():
    pprint(spending[doc])

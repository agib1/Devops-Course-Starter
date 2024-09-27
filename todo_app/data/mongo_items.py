import os
from todo_app.data.item import Item
import pymongo


def add_item(title):
    client = pymongo.MongoClient(os.getenv("CONNECTION_STRING"))
    db = client[os.getenv("DATABASE_NAME")]

    item = {
        "name" : title,
        "status" : "To Do"
    }

    db.items.insert_one(item)


def get_items():
    client = pymongo.MongoClient(os.getenv("CONNECTION_STRING"))
    db = client[os.getenv("DATABASE_NAME")]

    db_items = db.items.find()

    items = []

    for db_item in db_items:
            item = Item(db_item["_id"], db_item["name"], db_item["status"])
            items.append(item)

    return items


def move_item_to_done(item_id):
    client = pymongo.MongoClient(os.getenv("CONNECTION_STRING"))
    db = client[os.getenv("DATABASE_NAME")]

    db.items.find_one_and_update({"_id" : item_id}, {"$set" : {"status" : "Done"}})

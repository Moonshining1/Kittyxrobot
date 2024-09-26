from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pymongo import MongoClient, collection
from pymongo.errors import PyMongoError
from MukeshRobot import MONGO_DB_URI

# Create MongoDB async client
mongo = MongoCli(MONGO_DB_URI)
Mukeshdb = mongo.MUK_ROB

try:
    # Create MongoDB synchronous client
    client = MongoClient(MONGO_DB_URI)
except PyMongoError:
    exit(1)

main_db = client["MOON_SHINING_ROBOT"]
MukeshXdb = main_db


def get_collection(name: str) -> collection.Collection:
    """Get the collection from the database."""
    return MukeshXdb[name]


class MongoDB:
    """Class for interacting with the bot's MongoDB database."""

    def __init__(self, collection_name: str) -> None:
        self.collection = MukeshXdb[collection_name]

    # Insert one entry into the collection
    def insert_one(self, document: dict) -> str:
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    # Find one entry in the collection
    def find_one(self, query: dict):
        result = self.collection.find_one(query)
        if result:
            return result
        return None

    # Find all entries matching a query
    def find_all(self, query: dict = None) -> list:
        if query is None:
            query = {}
        return list(self.collection.find(query))

    # Count entries in the collection
    def count(self, query: dict = None) -> int:
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    # Delete entries matching a query
    def delete_one(self, query: dict) -> int:
        self.collection.delete_one(query)
        return self.collection.count_documents({})

    # Replace one document in the collection
    def replace(self, query: dict, new_data: dict) -> tuple:
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new

    # Update one document in the collection
    def update(self, query: dict, update_data: dict) -> tuple:
        result = self.collection.update_one(query, {"$set": update_data})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document

    @staticmethod
    def close():
        client.close()


# Ensure MongoDB connection is established at start
def __connect_first():
    _ = MongoDB("test")


__connect_first()

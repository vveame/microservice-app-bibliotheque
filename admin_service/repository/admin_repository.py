from bson.objectid import ObjectId
from extensions import mongo
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone

class AdminRepository:
    def __init__(self):
        self.collection = mongo.db.admins  # MongoDB collection

    def save(self, admin_dict):
        try:
            admin_dict["created_at"] = datetime.now(timezone.utc)
            admin_dict["updated_at"] = datetime.now(timezone.utc)
            result = self.collection.insert_one(admin_dict)
            admin_dict["_id"] = result.inserted_id
            return admin_dict
        except DuplicateKeyError:
            raise ValueError("Email already exists")

    def find_all(self):
        admins = self.collection.find()
        return list(admins)

    def find_by_id(self, id):
        admin = self.collection.find_one({"_id": ObjectId(id)})
        return admin

    def find_by_email(self, email):
        admin = self.collection.find_one({"email": email})
        return admin

    def update(self, id, update_dict):
        update_dict["updated_at"] = datetime.now(timezone.utc)
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_dict})
        return self.find_by_id(id)

    def delete(self, id):
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
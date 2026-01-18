# repository/bibliothecaire_repository.py

from bson.objectid import ObjectId
from extensions import mongo
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone

class BibliothecaireRepository:
    def __init__(self):
        self.collection = mongo.db.bibliothecaires  # MongoDB collection

    def save(self, bibliothecaire_dict):
        try:
            bibliothecaire_dict["created_at"] = datetime.now(timezone.utc)
            bibliothecaire_dict["updated_at"] = datetime.now(timezone.utc)
            result = self.collection.insert_one(bibliothecaire_dict)
            bibliothecaire_dict["_id"] = result.inserted_id
            return bibliothecaire_dict
        except DuplicateKeyError:
            raise ValueError("Email already exists")

    def find_all(self):
        bibliothecaires = self.collection.find()
        return list(bibliothecaires)

    def find_by_id(self, id):
        bibliothecaire = self.collection.find_one({"_id": ObjectId(id)})
        return bibliothecaire

    def find_by_email(self, email):
        bibliothecaire = self.collection.find_one({"email": email})
        return bibliothecaire

    def update(self, id, update_dict):
        update_dict["updated_at"] = datetime.now(timezone.utc)
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_dict})
        return self.find_by_id(id)

    def delete(self, id):
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
# repository/lecteur_repository.py

from bson.objectid import ObjectId
from extensions import mongo
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone

class LecteurRepository:
    def __init__(self):
        self.collection = mongo.db.lecteurs  # MongoDB collection

    def save(self, lecteur_dict):
        try:
            lecteur_dict["created_at"] = datetime.now(timezone.utc)
            lecteur_dict["updated_at"] = datetime.now(timezone.utc)
            result = self.collection.insert_one(lecteur_dict)
            lecteur_dict["_id"] = result.inserted_id
            return lecteur_dict
        except DuplicateKeyError:
            raise ValueError("Email already exists")

    def find_all(self):
        lecteurs = self.collection.find()
        return list(lecteurs)

    def find_by_id(self, id):
        lecteur = self.collection.find_one({"_id": ObjectId(id)})
        return lecteur

    def find_by_email(self, email):
        lecteur = self.collection.find_one({"email": email})
        return lecteur

    def update(self, id, update_dict):
        update_dict["updated_at"] = datetime.now(timezone.utc)
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_dict})
        return self.find_by_id(id)

    def delete(self, id):
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
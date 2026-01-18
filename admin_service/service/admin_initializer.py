# services/admin_initializer.py

from datetime import datetime
from bson.objectid import ObjectId
from security.password_utils import hash_password, verify_password
from repository.admin_repository import AdminRepository
from config import Config

class AdminInitializer:
    def __init__(self):
        self.repo = AdminRepository()

    def create_default_admin(self):
        """Create default admin user if it doesn't exist"""
        default_admin_email = Config.DEFAULT_ADMIN_EMAIL

        # Hash the default password
        hashed_password = hash_password(Config.DEFAULT_ADMIN_PASSWORD)

        # Check if admin already exists
        existing_admin = self.repo.find_by_email(default_admin_email)

        if existing_admin:
            print(f"Default admin already exists with ID: {existing_admin.get('_id')}")
            if verify_password(Config.DEFAULT_ADMIN_PASSWORD, hashed_password) is True:
                print("WARNING: Please change the default password immediately!")
            return existing_admin

        # Create admin document
        admin_data = {
            "nom": "Administrator",
            "prenom": "System",
            "date_naissance": datetime(1990, 1, 1),
            "email": default_admin_email,
            "password": hashed_password,
            "role": "ADMIN",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Insert into database
        result = self.repo.save(admin_data)

        print(f"Default admin created with ID: {result['_id']}")
        print(f"Login credentials:")
        print(f"Email: {default_admin_email}")
        print(f"Password: {Config.DEFAULT_ADMIN_PASSWORD}")
        print("WARNING: Please change the default password immediately!")

        return admin_data
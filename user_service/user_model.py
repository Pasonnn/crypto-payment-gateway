from db import Database
import datetime
import hashlib
import secrets
from bson.objectid import ObjectId

class UserModel:

    ### FIND USER ###
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return Database.get_collection("users").find_one({"email": email})
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        return Database.get_collection("users").find_one({"username": username})

    @staticmethod
    def find_by_id(user_id):

        """Find user by MongoDB ObjectID"""
        return Database.get_collection("users").find_one({"_id": user_id})
    ### END OF FIND USER ###

    ### HASH PASSWORD ###
    @staticmethod
    def hash_password(password):
        """Hash user password"""
        return hashlib.sha256(password.encode()).hexdigest()
    ### END OF HASH PASSWORD ###

    ### GENERATE API KEY ###
    @staticmethod
    def generate_api_key():
        """Generate a unique API key"""
        return secrets.token_hex(32)  # Generates a 64-character random API key
    ### END OF GENERATE API KEY ###

    ### INIT USER ###
    def __init__(self, username, email, password, role="user", wallet_address=""):
        """Initialize a new user object"""
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.wallet_address = wallet_address
        self.api_key = self.generate_api_key()  # Assign a new API key during registration
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
    ### END OF INIT USER ###

    ### CRUD OPERATIONS ###
    def save(self): 
        """Save the user to MongoDB"""
        user_collection = Database.get_collection("users")
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "wallet_address": self.wallet_address,
            "api_key": self.api_key,  # Store API key in database
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        user_collection.insert_one(user_data)

    @staticmethod
    def update_user(user_id, updates):
        """Update user details"""
        user_collection = Database.get_collection("users")
        updates["updated_at"] = datetime.datetime.utcnow()
        user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updates})

    @staticmethod
    def delete_user(user_id):
        """Delete a user"""
        user_collection = Database.get_collection("users")
        user_collection.delete_one({"_id": user_id})

    @staticmethod
    def regenerate_api_key(user_id):
        """Generate a new API key for the user"""
        new_api_key = secrets.token_hex(32)  # Generate a new API key
        user_collection = Database.get_collection("users")
        user_collection.update_one({"_id": user_id}, {"$set": {"api_key": new_api_key}})
        return new_api_key
    ### END OF CRUD OPERATIONS ###
from user_service.user_model import UserModel
from database.db import Database
from bson.objectid import ObjectId
import datetime
import jwt
import os
from flask import request, jsonify


class UserController:
    def __init__(self, db_uri, db_name):
        self.database = Database(db_uri, db_name)  # Create an instance of Database

    @staticmethod
    def register(data):
        """Register a new user with username, email, password (No Auth Required)"""
        try:
            # Create an instance Database to access the collection
            db = Database.get_collection("users")

            # Get the data from the request
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Check if all required fields are provided
            if not username or not email or not password:
                return jsonify({"error": "Missing required fields"}), 400

            # Check if username or email already exists
            existing_user = UserModel.find_by_email(email)
            if existing_user:

                return jsonify({"error": "Email already in use"}), 400
            
            existing_user = UserModel.find_by_username(username)
            if existing_user:
                return jsonify({"error": "Username already in use"}), 400
            
            # Hash the password
            hashed_password = UserModel.hash_password(password)

            # Create a new user
            user = UserModel(username, email, hashed_password)

            # Save the user to the database
            user.save()

            return jsonify({"message": "User registered successfully"}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def login(data):
        """Login a user with email, password (No Auth Required)"""
        try:
            # Get the data from the request
            email = data.get("email")
            password = data.get("password")

            # Check if all required fields are provided
            if not email or not password:
                return jsonify({"error": "Missing required fields"}), 400

            # Find the user by email
            user = UserModel.find_by_email(email)

            # Check if user exists
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Check if the password is correct
            if UserModel.hash_password(password) != user['password']:
                return jsonify({"error": "Invalid password"}), 401
            
            # Generate a JWT token
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            token_payload = {
                "user_id": str(user["_id"]),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Expires in 24 hours
            }
            token = jwt.encode(token_payload, secret_key, algorithm="HS256")

            # Return the token
            return jsonify({"status": "success", "token": token}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def get_profile(request):
        """Get current user profile (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Convert the _id to a string
            user["_id"] = str(user["_id"])

            # Remove password field from response
            user.pop("password", None)

            return jsonify({"user": user}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    @staticmethod
    def get_api_key(request):
        """Get current user API key (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Convert the _id to a string
            user["_id"] = str(user["_id"])

            # Get the API key
            api_key = user.get("api_key")

            # Return the user object
            return jsonify({"api_key": api_key}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    @staticmethod
    def regenerate_api_key(data):
        """Regenerate current user API key (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Generate a new API key
            new_api_key = UserModel.generate_api_key()

            # Update the user with the new API key
            UserModel.update_user(ObjectId(user_id), {"api_key": new_api_key})

            return jsonify({"message": "API key regenerated successfully", "api_key": new_api_key}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def edit_user(data):
        """Edit current user profile: username, password (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"]) 
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))  

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Get the data from the request
            username = data.get("username")
            password = data.get("password")

            # Check if all required fields are provided
            if not username and not password:
                return jsonify({"error": "Missing required fields"}), 400
            elif not username:
                username = user["username"]
            elif not password:  
                password = user["password"]

            if username == user["username"] and password == user["password"]:
                return jsonify({"error": "No changes made"}), 400

            # Hash the password
            hashed_password = UserModel.hash_password(password)


            # Update the user with the new username and password
            UserModel.update_user(ObjectId(user_id), {"username": username, "password": hashed_password})

            return jsonify({"message": "User updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_me(data):
        """Delete current user (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id)) 

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Delete the user
            UserModel.delete_user(ObjectId(user_id))

            return jsonify({"message": "User deleted successfully"}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def update_wallet(data):
        """Update current user wallet address (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Get the wallet address from the request
            wallet_address = data.get("wallet_address")

            # Check if the wallet address is valid
            if not wallet_address:
                return jsonify({"error": "Invalid wallet address"}), 400

            if wallet_address == user["wallet_address"]:
                return jsonify({"error": "No changes made"}), 400

            # Update the user with the new wallet address
            UserModel.update_user(ObjectId(user_id), {"wallet_address": wallet_address})


            return jsonify({"message": "Wallet address updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def get_dashboard(request):
        """Get current user dashboard data: revenue, transactions, wallet details, etc. (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            
            user_id = decoded_token.get("user_id")
            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            print(f"user_id: {user_id}")

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            # Get dashboard data from database
            db_payments = Database.get_collection("payments")
            payments = db_payments.find({"user_id": ObjectId(user_id)})
            payments_list = list(payments)
            print(f"payments_list: {payments_list}")

            total_revenue = 0
            total_transactions = 0
            total_fee = 0

            for payment in payments_list:
                payment_revenue = payment["amount"]
                payment_fee = payment["fee"]
                total_revenue += payment_revenue
                total_transactions += 1
                total_fee += payment_fee

            # Calculate the total revenue
            # Dashboard data

            dashboard_data = {
                "revenue": total_revenue,
                "transactions": total_transactions,
                "fee": total_fee,
            }

            return jsonify({"dashboard": dashboard_data}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_transactions(request):
        """Get all current user transactions (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Get the transactions from the database
            db_payments = Database.get_collection("payments")
            transactions = db_payments.find({"user_id": ObjectId(user_id)})
            transactions_list = list(transactions)
            print(f"transactions_list: {transactions_list}")


            transactions_data = {}

            for transaction in transactions_list:
                transactions_data[str(transaction["_id"])] = {
                    "amount": transaction["amount"],
                    "fee": transaction["fee"],
                    "status": transaction["status"],
                    "created_at": transaction["created_at"],
                    "updated_at": transaction["updated_at"]
                }


            return jsonify({"transactions": transactions_data}), 200


        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def get_users(request):
        """Get all users (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            if user["role"] != "admin":
                return jsonify({"error": "Unauthorized"}), 403

            # Get the users from the database
            db_users = Database.get_collection("users")
            users = db_users.find()
            users_list = list(users)

            users_data = {}
            for user in users_list:
                users_data[str(user["_id"])] = {
                    "username": user["username"],
                    "email": user["email"],
                    "role": user["role"],
                    "wallet_address": user["wallet_address"],
                    "created_at": user["created_at"],
                    "updated_at": user["updated_at"]
                }  


            return jsonify({"users": users_data}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user(user_id):
        """Get a specific user by ID (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            if user["role"] != "admin":
                return jsonify({"error": "Unauthorized"}), 403

            user_data = {
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
                "wallet_address": user["wallet_address"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"]
            }

            return jsonify({"user": user_data}), 200


        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_user(user_id):
        """Delete a specific user by ID (JWT Auth Required)"""
        try:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404

            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            if user["role"] != "admin":
                return jsonify({"error": "Unauthorized"}), 403
            
            # Delete the user
            UserModel.delete_user(ObjectId(user_id))

            return jsonify({"message": "User deleted successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    
    
    







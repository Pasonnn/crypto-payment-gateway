from user_service.user_model import UserModel
from db import Database
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
            ### GET DATA FROM REQUEST AND VALIDATE ###
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
            ### END OF DATA VALIDATION ###

            ### HASH PASSWORD ###
            # Hash the password
            hashed_password = UserModel.hash_password(password)
            ### END OF HASH PASSWORD ###

            ### CREATE USER ###
            # Create a new user
            user = UserModel(username, email, hashed_password)
            ### END OF CREATE USER ###

            ### SAVE USER TO DATABASE ###
            # Save the user to the database
            user.save()
            ### END OF SAVE USER TO DATABASE ###

            return jsonify({"message": "User registered successfully"}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def login(data):
        """Login a user with email, password (No Auth Required)"""
        try:
            ### GET DATA FROM REQUEST AND VALIDATE ###
            # Get the data from the request
            email = data.get("email")
            password = data.get("password")

            # Check if all required fields are provided
            if not email or not password:
                return jsonify({"error": "Missing required fields"}), 400
            ### END OF DATA VALIDATION ###

            ### FIND USER BY EMAIL ###
            # Find the user by email
            user = UserModel.find_by_email(email)
            ### END OF FIND USER BY EMAIL ###

            ### CHECK IF USER EXISTS ###
            # Check if user exists
            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF CHECK IF USER EXISTS ###

            ### CHECK IF PASSWORD IS CORRECT ###
            # Check if the password is correct
            if UserModel.hash_password(password) != user['password']:
                return jsonify({"error": "Invalid password"}), 401
            ### END OF CHECK IF PASSWORD IS CORRECT ###
            
            ### GENERATE JWT TOKEN ###
            # Generate a JWT token
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            token_payload = {
                "user_id": str(user["_id"]),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Expires in 24 hours
            }
            token = jwt.encode(token_payload, secret_key, algorithm="HS256")
            ### END OF GENERATE JWT TOKEN ###

            ### RETURN SUCCESS RESPONSE ###
            # Return the token
            return jsonify({"status": "success", "token": token}), 200
            ### END OF RETURN SUCCESS RESPONSE ###

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_profile(request):
        """Get current user profile (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
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
            ### END OF GET JWT TOKEN FROM REQUEST ###

            ### CHECK IF USER ID IS FOUND IN TOKEN ###
            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF CHECK IF USER ID IS FOUND IN TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### DATA OUTPUT PROCESSING ###
            # Convert the _id to a string
            user["_id"] = str(user["_id"])

            # Remove password field from response
            user.pop("password", None)
            ### END OF DATA OUTPUT PROCESSING ###

            # Return the user object
            return jsonify({"user": user}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def get_api_key(request):
        """Get current user API key (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            ### END OF GET JWT TOKEN FROM REQUEST ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### DATA OUTPUT PROCESSING ###
            # Convert the _id to a string
            user["_id"] = str(user["_id"])
            ### END OF DATA OUTPUT PROCESSING ###

            ### GET API KEY ###
            # Get the API key
            api_key = user.get("api_key")
            ### END OF GET API KEY ###

            # Return the user object
            return jsonify({"api_key": api_key}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def regenerate_api_key(data):
        """Regenerate current user API key (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            ### END OF GET JWT TOKEN FROM REQUEST ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### GENERATE NEW API KEY ###
            # Generate a new API key
            new_api_key = UserModel.generate_api_key()
            ### END OF GENERATE NEW API KEY ###

            ### UPDATE USER WITH NEW API KEY ###
            # Update the user with the new API key
            UserModel.update_user(ObjectId(user_id), {"api_key": new_api_key})
            ### END OF UPDATE USER WITH NEW API KEY ###

            # Return the new API key
            return jsonify({"message": "API key regenerated successfully", "api_key": new_api_key}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def edit_user(data):
        """Edit current user profile: username, password (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):

                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"]) 
            ### END OF DECODE JWT TOKEN ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))  

            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### GET DATA FROM REQUEST ###
            # Get the data from the request
            username = data.get("username")
            password = data.get("password")
            ### END OF GET DATA FROM REQUEST ###

            ### CHECK IF ALL REQUIRED FIELDS ARE PROVIDED ###
            # Check if all required fields are provided
            if not username and not password:
                return jsonify({"error": "Missing required fields"}), 400
            elif not username:
                username = user["username"]
            elif not password:  
                password = user["password"]

            if username == user["username"] and password == user["password"]:
                return jsonify({"error": "No changes made"}), 400
            ### END OF CHECK IF ALL REQUIRED FIELDS ARE PROVIDED ###

            ### HASH PASSWORD ###
            # Hash the password
            hashed_password = UserModel.hash_password(password)
            ### END OF HASH PASSWORD ###

            ### UPDATE USER WITH NEW USERNAME AND PASSWORD ###
            # Update the user with the new username and password
            UserModel.update_user(ObjectId(user_id), {"username": username, "password": hashed_password})
            ### END OF UPDATE USER WITH NEW USERNAME AND PASSWORD ###

            # Return the success message
            return jsonify({"message": "User updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_me(data):
        """Delete current user (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            ### END OF DECODE JWT TOKEN ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")
            print(f"user_id: {user_id}")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id)) 

            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### DELETE USER FROM DATABASE ###
            # Delete the user
            UserModel.delete_user(ObjectId(user_id))
            ### END OF DELETE USER FROM DATABASE ###

            # Return the success message
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
            ### END OF DECODE JWT TOKEN ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))

            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### GET DATA FROM REQUEST ###
            # Get the wallet address from the request
            wallet_address = data.get("wallet_address")
            ### END OF GET DATA FROM REQUEST ###

            ### CHECK IF WALLET ADDRESS IS VALID ###
            # Check if the wallet address is valid
            if not wallet_address:
                return jsonify({"error": "Invalid wallet address"}), 400
            ### END OF CHECK IF WALLET ADDRESS IS VALID ###

            ### CHECK NEW WALLET ADDRESS AND CURRENT WALLET ADDRESS ###
            # Check if the wallet address is the same as the current wallet address
            if wallet_address == user["wallet_address"]:
                return jsonify({"error": "No changes made"}), 400
            ### END OF CHECK NEW WALLET ADDRESS AND CURRENT WALLET ADDRESS ###

            ### UPDATE USER WITH NEW WALLET ADDRESS ###
            # Update the user with the new wallet address
            UserModel.update_user(ObjectId(user_id), {"wallet_address": wallet_address})
            ### END OF UPDATE USER WITH NEW WALLET ADDRESS ###

            # Return the success message
            return jsonify({"message": "Wallet address updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_dashboard(request):
        """Get current user dashboard data: revenue, transactions, wallet details, etc. (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):

                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            ### END OF DECODE JWT TOKEN ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")
            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### GET DASHBOARD DATA FROM DATABASE ###
            # Get dashboard data from database
            db_payments = Database.get_collection("payments")
            payments = db_payments.find({"user_id": ObjectId(user_id)})
            payments_list = list(payments)
            ### END OF GET DASHBOARD DATA FROM DATABASE ###

            ### CALCULATE DASHBOARD DATA ###
            total_revenue = 0
            total_transactions = 0
            total_fee = 0

            for payment in payments_list:
                payment_revenue = payment["amount"]
                payment_fee = payment["fee"]
                total_revenue += payment_revenue
                total_transactions += 1
                total_fee += payment_fee
            ### END OF CALCULATE DASHBOARD DATA ###

            ### CREATE DASHBOARD DATA ###
            # Dashboard data
            dashboard_data = {
                "revenue": total_revenue,
                "transactions": total_transactions,
                "fee": total_fee,
            }
            ### END OF CREATE DASHBOARD DATA ###

            # Return the dashboard data
            return jsonify({"dashboard": dashboard_data}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_transactions(request):
        """Get all current user transactions (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            ### END OF DECODE JWT TOKEN ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### GET TRANSACTIONS FROM DATABASE ###
            # Get the transactions from the database
            db_payments = Database.get_collection("payments")
            transactions = db_payments.find({"user_id": ObjectId(user_id)})
            transactions_list = list(transactions)
            ### END OF GET TRANSACTIONS FROM DATABASE ###

            ### CREATE TRANSACTIONS DATA ###
            transactions_data = {}

            for transaction in transactions_list:
                transactions_data[str(transaction["_id"])] = {
                    "payment_address": transaction["payment_address"],
                    "payment_address_private_key": transaction["payment_address_private_key"],
                    "amount": transaction["amount"],
                    "fee": transaction["fee"],
                    "status": transaction["status"],
                    "created_at": transaction["created_at"],
                    "updated_at": transaction["updated_at"]
                }
            ### END OF CREATE TRANSACTIONS DATA ###

            # Return the transactions data
            return jsonify({"transactions": transactions_data}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_users(request):
        """Get all users (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            ### END OF DECODE JWT TOKEN ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")


            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### CHECK IF USER IS ADMIN ###
            if user["role"] != "admin":
                return jsonify({"error": "Unauthorized"}), 403
            ### END OF CHECK IF USER IS ADMIN ###

            ### GET USERS FROM DATABASE ###
            # Get the users from the database
            db_users = Database.get_collection("users")
            users = db_users.find()
            users_list = list(users)
            ### END OF GET USERS FROM DATABASE ###

            ### CREATE USERS DATA ###
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
            ### END OF CREATE USERS DATA ###

            # Return the users data
            return jsonify({"users": users_data}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user(user_id):
        """Get a specific user by ID (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            ### END OF DECODE JWT TOKEN ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### CHECK IF USER IS ADMIN ###
            if user["role"] != "admin":
                return jsonify({"error": "Unauthorized"}), 403
            ### END OF CHECK IF USER IS ADMIN ###

            ### CREATE USER DATA ###
            user_data = {
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
                "wallet_address": user["wallet_address"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"]
            }
            ### END OF CREATE USER DATA ###

            # Return the user data
            return jsonify({"user": user_data}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_user(user_id):
        """Delete a specific user by ID (JWT Auth Required)"""
        try:
            ### GET JWT TOKEN FROM REQUEST ###
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Invalid or missing Authorization token."}), 401

            # Get the token by removing the "Bearer " prefix
            token = auth_header.split(" ")[1]

            # Decode the JWT token safely
            secret_key = os.getenv("SECRET_KEY", "defaultsecret")
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            ### END OF DECODE JWT TOKEN ###

            ### GET USER ID FROM TOKEN ###
            user_id = decoded_token.get("user_id")

            if not user_id:
                return jsonify({"error": "User ID not found in token"}), 404
            ### END OF GET USER ID FROM TOKEN ###

            ### FIND USER BY ID AND CHECK IF USER EXISTS ###
            # Ensure the ID is an ObjectId
            user = UserModel.find_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404
            ### END OF FIND USER BY ID AND CHECK IF USER EXISTS ###

            ### CHECK IF USER IS ADMIN ###
            if user["role"] != "admin":
                return jsonify({"error": "Unauthorized"}), 403
            ### END OF CHECK IF USER IS ADMIN ###

            ### DELETE USER FROM DATABASE ###
            # Delete the user
            UserModel.delete_user(ObjectId(user_id))
            ### END OF DELETE USER FROM DATABASE ###

            # Return the success message
            return jsonify({"message": "User deleted successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


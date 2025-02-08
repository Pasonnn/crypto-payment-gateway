from flask import Blueprint, request, jsonify
from user_service.user_controller import UserController

user_routes = Blueprint("users", __name__)


### Health Check Route ###
@user_routes.route('/api/users/health', methods=['GET'])
def health():
    """Health check route"""
    # Input: None
    # Process: Check if the user service is running
    # Output: JSON response with status "User Service is running"
    return {"status": "User Service is running"}, 200
### END OF HEALTH CHECK ROUTE ###


### User Authentication Routes ###
@user_routes.route("/api/users/register", methods=["POST"])
def register():
    """Register a new user with username, email, password (No Auth Required)"""
    # Input: JSON object with the following fields:
    # - username: string
    # - email: string
    # - password: string
    # Process: Register a new user in the database
    # Output: JSON response with the success message
    # Output Expected Fields:
    # - message: string
    data = request.json
    return UserController.register(data)

@user_routes.route("/api/users/login", methods=["POST"])
def login():
    """Login a user with email, password (No Auth Required)"""
    # Input: JSON object with the following fields:
    # - email: string
    # - password: string
    # Process: Login a user in the database
    # Output: JSON response with the success message
    # Output Expected Fields:
    # - status: string
    # - token: string
    data = request.json
    return UserController.login(data)



@user_routes.route("/api/users/profile", methods=["GET"])
def get_profile():
    """Get current user profile (JWT Auth Required)"""
    # Input: None
    # Process: Get the current user profile from the database
    # Output: JSON response with the user object
    # Output Expected Fields:
    # - _id: ObjectId
    # - username: string
    # - email: string
    # - wallet_address: string
    # - role: string
    # - api_key: string
    # - created_at: string
    # - updated_at: string
    return UserController.get_profile(request)


### API Key Management Routes ###
@user_routes.route("/api/users/api_key", methods=["GET"])
def get_api_key():
    """Get current user API key (JWT Auth Required)"""
    # Input: None
    # Process: Get the current user API key from the database
    # Output: JSON response with the user object
    # Output Expected Fields:
    # - api_key: string
    return UserController.get_api_key(request)



@user_routes.route("/api/users/regenerate_api_key", methods=["POST"])
def regenerate_api_key():
    """Regenerate current user API key (JWT Auth Required)"""
    # Input: None
    # Process: Regenerate the current user API key
    # Output: JSON response
    # Output Expected Fields:
    # - message: string
    # - api_key: string
    return UserController.regenerate_api_key(request)



### User Management Routes ###
@user_routes.route("/api/users/edit", methods=["PUT"])
def edit_user():
    """Edit current user profile: username, password (JWT Auth Required)"""
    # Input: JSON object with the following fields:
    # - username: string (optional)
    # - password: string (optional)
    # Process: Edit the current user profile in the database
    # Output: JSON response
    # Output Expected Fields:
    # - message: string
    data = request.json
    return UserController.edit_user(data)


@user_routes.route("/api/users/delete", methods=["DELETE"])
def delete_me():
    """Delete current user (JWT Auth Required)"""
    # Input: None
    # Process: Delete the current user from the database
    # Output: JSON response
    # Output Expected Fields:
    # - message: string
    return UserController.delete_me(request)



### User Wallet & Payment Management Routes ###
@user_routes.route("/api/users/update_wallet", methods=["PUT"])
def update_wallet():
    """Update current user wallet address (JWT Auth Required)"""
    # Input: JSON object with the following fields:
    # - wallet_address: string
    # Process: Update the current user wallet address in the database
    # Output: JSON response
    # Output Expected Fields:
    # - message: string
    data = request.json
    return UserController.update_wallet(data)



### Transaction & Dashboard Management Routes ###
@user_routes.route("/api/users/dashboard", methods=["GET"])
def get_dashboard():
    """Get current user dashboard data: revenue, transactions, fee, etc. (JWT Auth Required)"""
    # Input: None
    # Process: Get the current user dashboard data from the database
    # Output: JSON response
    # Output Expected Fields:
    # - revenue: number
    # - transactions: number
    # - fee: number
    return UserController.get_dashboard(request)


@user_routes.route("/api/users/transactions", methods=["GET"])
def get_transactions():
    """Get all current user transactions (JWT Auth Required)"""
    # Input: None
    # Process: Get all the current user transactions from the database
    # Output: JSON response
    # Output Expected Fields:
    # - transactions: list of transactions
    return UserController.get_transactions(request)



### Admin Routes ###
@user_routes.route("/api/admin/users", methods=["GET"])
def get_users():
    """Get all users (JWT Auth Required)"""
    # Input: None
    # Process: Get all the users from the database
    # Output: JSON response
    # Output Expected Fields:
    # - users: list of users
    return UserController.get_users(request)



@user_routes.route("/api/admin/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by ID (JWT Auth Required)"""
    # Input: user_id: string
    # Process: Get a specific user by ID from the database
    # Output: JSON response
    # Output Expected Fields:
    # - _id: ObjectId
    # - username: string
    # - email: string
    # - wallet_address: string
    # - role: string
    # - api_key: string
    # - created_at: string
    # - updated_at: string
    return UserController.get_user(user_id)



@user_routes.route("/api/admin/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a specific user by ID (JWT Auth Required)"""
    # Input: user_id: string
    # Process: Delete a specific user by ID from the database
    # Output: JSON response
    # Output Expected Fields:
    # - message: string
    return UserController.delete_user(user_id)
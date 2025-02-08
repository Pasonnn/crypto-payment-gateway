from flask import Blueprint, request, jsonify
from user_service.user_controller import UserController

user_routes = Blueprint("users", __name__)

@user_routes.route('/api/users/health', methods=['GET'])
def health():
    """Health check route"""
    return {"status": "User Service is running"}, 200

### User Authentication Routes ###

@user_routes.route("/api/users/register", methods=["POST"])
def register():
    """Register a new user with username, email, password (No Auth Required)"""
    data = request.json
    return UserController.register(data)

@user_routes.route("/api/users/login", methods=["POST"])
def login():
    """Login a user with email, password (No Auth Required)"""
    data = request.json
    return UserController.login(data)


@user_routes.route("/api/users/profile", methods=["GET"])
def get_profile():
    """Get current user profile (JWT Auth Required)"""
    return UserController.get_profile(request)




### API Key Management Routes ###

@user_routes.route("/api/users/api_key", methods=["GET"])
def get_api_key():
    """Get current user API key (JWT Auth Required)"""
    return UserController.get_api_key(request)


@user_routes.route("/api/users/regenerate_api_key", methods=["POST"])
def regenerate_api_key():
    """Regenerate current user API key (JWT Auth Required)"""
    return UserController.regenerate_api_key(request)


### User Management Routes ###

@user_routes.route("/api/users/edit", methods=["PUT"])
def edit_user():
    """Edit current user profile: username, password (JWT Auth Required)"""
    data = request.json
    return UserController.edit_user(data)


@user_routes.route("/api/users/delete", methods=["DELETE"])
def delete_me():
    """Delete current user (JWT Auth Required)"""
    data = request.json
    return UserController.delete_me(data)




### User Wallet & Payment Management Routes ###

@user_routes.route("/api/users/update_wallet", methods=["PUT"])
def update_wallet():
    """Update current user wallet address (JWT Auth Required)"""
    data = request.json
    return UserController.update_wallet(data)


### Transaction & Dashboard Management Routes ###

@user_routes.route("/api/users/dashboard", methods=["GET"])
def get_dashboard():
    """Get current user dashboard data: revenue, transactions, wallet details, etc. (JWT Auth Required)"""
    return UserController.get_dashboard(request)

@user_routes.route("/api/users/transactions", methods=["GET"])
def get_transactions():
    """Get all current user transactions (JWT Auth Required)"""
    return UserController.get_transactions(request)


### Admin Routes ###

@user_routes.route("/api/admin/users", methods=["GET"])
def get_users():
    """Get all users (JWT Auth Required)"""
    return UserController.get_users(request)


@user_routes.route("/api/admin/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by ID (JWT Auth Required)"""
    return UserController.get_user(user_id)


@user_routes.route("/api/admin/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a specific user by ID (JWT Auth Required)"""
    return UserController.delete_user(user_id)
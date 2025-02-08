# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from web3 import Web3
from payment_service.payment_routes import payment_routes
from user_service.user_routes import user_routes
from database.db import Database

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure secret key
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

# Initialize Database
Database() 

# Register User Routes
app.register_blueprint(payment_routes)
app.register_blueprint(user_routes)

@app.route('/health', methods=['GET'])
def health():
    """Health check route"""
    return {"status": "API Gateway is running"}, 200

# Run Flask Server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
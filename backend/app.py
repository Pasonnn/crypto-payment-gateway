from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from web3 import Web3

# ✅ Load Environment Variables
load_dotenv()

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)

# ✅ Ensure "database/" folder exists
if not os.path.exists("database"):
    os.makedirs("database")

# ✅ Secure Configurations
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

# ✅ Connect to Infura Ethereum Node
INFURA_URL = os.getenv("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# ✅ Check Ethereum Connection
if w3.is_connected():
    print("✅ Connected to Ethereum!")
else:
    print("❌ Failed to connect to Ethereum!")

# ✅ Home Route
@app.route("/")
def home():
    return jsonify({"message": "Crypto Payment Gateway API is running!"})

# ✅ Import & Register Payment Routes
from routes.payment_routes import payment_routes
app.register_blueprint(payment_routes)

# ✅ Run Flask Server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

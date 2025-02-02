from flask import Flask, jsonify
from flask_cors import CORS
import os
import os.path
from routes.payment_routes import payment_routes
from database.models import db

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# "database/" folder set up
DATABASE_DIR = "database"
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

# Load Configurations
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/payments.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db.init_app(app)

with app.app_context():
    db.create_all()

# Home Route
@app.route("/")
def home():
    return jsonify({"message": "Crypto Payment Gateway API is running!"})

# Register Routes
app.register_blueprint(payment_routes)

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

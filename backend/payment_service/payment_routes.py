from flask import Blueprint, request, jsonify
from payment_service.payment_controller import PaymentController


payment_routes = Blueprint("payments", __name__)

@payment_routes.route('/api/payments/health', methods=['GET'])
def health():
    """Health check route"""
    # Input: None
    # Process: Check if the payment service is running
    # Output: JSON response with status "Payment Service is running"
    return {"status": "Payment Service is running"}, 200

@payment_routes.route("/api/payments/create_payment", methods=["POST"])
def create_payment():
    """Create a new crypto payment request (API Key Auth Required)"""
    # Input: JSON object with the following fields:
    # - api_key: string
    # - amount: float
    # - currency: string
    # Process: Create a new payment object in the database
    # Output: JSON response with the payment object 
    # Output Expected Fields:
    # - eth_amount: float
    # - payment_address: string
    data = request.json
    return PaymentController.create_payment(data)



@payment_routes.route("/api/payments/update_payment_status", methods=["PUT"])
def update_payment_status():
    """Update the status of a payment (API Key Auth Required)"""
    # Input: JSON object with the following fields:
    # - payment_address: string
    # - api_key: string
    # Process: Update the status of a payment to success in the database and send the funds to the user/admin
    # Output: JSON response with the payment object
    # Output Expected Fields:
    # - status: string
    data = request.json
    return PaymentController.update_payment_status(data)



@payment_routes.route("/api/payments/payment_status", methods=["GET"])
def payment_status():
    """Get payment status for a given payment ID (NO API Key Auth Required)"""
    # Input: Query parameter payment_address
    # Process: Get the payment status from the database
    # Output: JSON response with the payment object
    # Output Expected Fields:
    # - status: string
    payment_address = request.args.get('payment_address')
    return PaymentController.payment_status(payment_address)

@payment_routes.route("/api/payments/timeout", methods=["PUT"])
def timeout():
    """Get the timeout for a given payment ID (NO API Key Auth Required)"""
    # Input: JSON object with the following fields:
    # - payment_address: string
    # - api_key: string
    # Process: Get the timeout for a given payment ID from the database
    # Output: JSON response with the timeout
    # Output Expected Fields:
    # - status: string
    data = request.json
    return PaymentController.timeout(data)



from flask import Blueprint, request, jsonify
from payment_service.payment_controller import PaymentController


payment_routes = Blueprint("payments", __name__)

@payment_routes.route('/api/payments/health', methods=['GET'])
def health():
    """Health check route"""
    return {"status": "Payment Service is running"}, 200

@payment_routes.route("/api/payments/create_payment", methods=["POST"])
def create_payment():
    """Create a new crypto payment request (API Key Auth Required)"""
    data = request.json
    return PaymentController.create_payment(data)

@payment_routes.route("/api/payments/update_payment_status", methods=["PUT"])
def update_payment_status():
    """Update the status of a payment (API Key Auth Required)"""
    data = request.json
    return PaymentController.update_payment_status(data)

@payment_routes.route("/api/payments/payment_status", methods=["GET"])
def payment_status():
    """Get payment status for a given payment ID (NO API Key Auth Required)"""
    payment_address = request.args.get('payment_address')
    return PaymentController.payment_status(payment_address)
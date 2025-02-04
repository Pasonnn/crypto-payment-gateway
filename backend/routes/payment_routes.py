from flask import Blueprint, request, jsonify
from blockchain.web3_utils import (
    generate_wallet,
    get_transaction_status,
    convert_usd_to_eth,
    check_eth_balance,
    monitor_eth_payment
)

payment_routes = Blueprint("payments", __name__)

# ✅ Generate a Payment Request
@payment_routes.route("/api/payment/init", methods=["POST"])
def init_payment():
    """Creates a new ETH payment request"""
    data = request.json
    amount_usd = data.get("amount")

    if not amount_usd:
        return jsonify({"status": "error", "message": "Amount in USD is required"}), 400

    wallet = generate_wallet()
    amount_eth = convert_usd_to_eth(amount_usd)

    if amount_eth is None:
        return jsonify({"status": "error", "message": "Failed to get ETH price"}), 500

    return jsonify({
        "status": "waiting_for_payment",
        "payment_address": wallet["address"],
        "amount_eth": amount_eth,
        "amount_usd": amount_usd
    })

# ✅ Check Payment Status
@payment_routes.route("/api/payment/status", methods=["GET"])
def payment_status():
    """Checks if the ETH payment has been received"""
    payment_address = request.args.get("payment_address")
    required_eth = request.args.get("required_eth")

    if not payment_address or not required_eth:
        return jsonify({"status": "error", "message": "Missing payment_address or required_eth"}), 400

    required_eth = float(required_eth)
    balance_eth = check_eth_balance(payment_address)

    if balance_eth >= required_eth:
        return jsonify({"status": "confirmed", "message": "Payment received!"})
    elif balance_eth > 0:
        return jsonify({"status": "partial_payment", "message": f"Received {balance_eth} ETH, waiting for full amount."})
    else:
        return jsonify({"status": "pending", "message": "No payment received yet."})

# ✅ Monitor ETH Payments for 10 Minutes
@payment_routes.route("/api/payment/monitor", methods=["POST"])
def monitor_payment():
    """Monitors ETH balance for payment completion"""
    data = request.json
    payment_address = data.get("payment_address")
    required_eth = data.get("required_eth")

    if not payment_address or not required_eth:
        return jsonify({"status": "error", "message": "Missing payment_address or required_eth"}), 400

    required_eth = float(required_eth)

    # ✅ Start Monitoring ETH Balance
    result = monitor_eth_payment(payment_address, required_eth)
    return jsonify(result)

# ✅ Generate a New Wallet
@payment_routes.route("/api/payment/wallet", methods=["GET"])
def create_wallet():
    """Creates a new Ethereum wallet"""
    wallet = generate_wallet()
    return jsonify(wallet)

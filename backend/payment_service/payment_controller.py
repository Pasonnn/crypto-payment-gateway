from payment_service.payment_model import PaymentModel
from database.db import Database
import requests
from web3 import Web3
import os
from flask import jsonify, request


w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_SEPOLIA_URL")))

class PaymentController:

    
    @staticmethod
    def create_payment(data):
        """Create a new crypto payment request (API Key Auth Required)""" 
        try:
            ### DATABASE CONNECTION ###
            # Create an instance Database to access the collection
            db_users = Database.get_collection("users")
            ### END OF DATABASE CONNECTION ###

            ### DATA PROCESSING ###
            # Get the data from the request 
            amount = data.get("amount")
            currency = data.get("currency")
            api_key = data.get("api_key")

            # Typecast the amount to a float
            try:
                amount = float(amount)
            except ValueError:
                return jsonify({"error": "Invalid amount"}), 400

            # Check if the API key is valid
            user = db_users.find_one({"api_key": api_key})
            if not user:


                return jsonify({"error": "Invalid API key"}), 401
            
            # Return the user id
            user_id = user["_id"]
            ### END OF DATA PROCESSING ###
            
            ### CURRENCY VALIDATION ###
            # Check if the amount is valid
            if amount <= 0:
                return jsonify({"error": "Invalid amount"}), 400
            
            # Check if the currency is valid
            if currency not in ["ETH"]:
                return jsonify({"error": "Invalid currency"}), 400

            # Convert the amount to ETH
            eth_amount = PaymentController.convert_usd_to_eth(amount)

            # Check if the ETH amount is valid
            if eth_amount is None:
                return jsonify({"error": "Invalid amount"}), 400
            ### END OF CURRENCY VALIDATION ###

            ### CREATE A NEW PAYMENT ADDRESS ###
            # Generate a private key
            private_key = PaymentModel.generate_private_key()
            # Generate a payment address
            payment_address = PaymentModel.generate_payment_address(private_key)
            ### END OF PAYMENT ADDRESS CREATION ###

            ### FEE CALCULATION ###
            # Calculate the fee
            fee = eth_amount * 0.01
            # Calculate the gas price
            gas_price = w3.eth.gas_price
            # Calculate the gas limit
            gas_limit = 21000
            gas_fee = gas_price * gas_limit/10**18
            # Calculate the total fee
            total_fee = fee + gas_fee*10
            ### END OF FEE CALCULATION ###



            payment = PaymentModel(user_id, 
                                   payment_address, 
                                   private_key, 
                                   eth_amount, 
                                   total_fee)
            

            # Save the payment to the database
            payment.save()

            return jsonify({"payment_address": payment_address, "eth_amount": eth_amount}), 200


        except Exception as e:
            print(f"Error creating payment: {e}")
            return jsonify({"error": "Error creating payment"}), 500


    @staticmethod
    def update_payment_status(data):
        """Update the status of a payment"""
        try:
            ### DATABASE CONNECTION ###
            db_users = Database.get_collection("users")
            ### END OF DATABASE CONNECTION ###

            # Get the API key from the request
            api_key = data.get("api_key")
            user = db_users.find_one({"api_key": api_key})
            if not user:
                return jsonify({"error": "Invalid API key"}), 401
            
            print(user["_id"])
            
            # Get the payment from the database
            payment_address = data.get("payment_address")
            payment = PaymentModel.find_by_payment_address(payment_address)
            if not payment:

                return jsonify({"error": "Payment not found"}), 404
            
            # Get the balance of the payment address
            balance_eth = PaymentController.check_eth_balance(payment_address)

            if balance_eth > payment["amount"]:
                # Update the status of the payment

                PaymentModel.update_payment(payment["_id"], {"status": "paid"})
                #TODO: Send money back to user wallet and fee to admin wallet
                # fund_distribute(amount, user_wallet, admin_wallet)

                return jsonify({"status": "Payment paid successfully"}), 200
            else:
                return jsonify({"status": "Payment not paid"}), 400
        except Exception as e:
            print(f"Error updating payment status: {e}")
            return jsonify({"error": "Error updating payment status"}), 500


    @staticmethod
    def payment_status(payment_address):
        """Get the status of a payment (API Key Auth Required)"""
        try:
            # Get the payment from the database
            payment = PaymentModel.find_by_payment_address(payment_address)
            if not payment:
                return jsonify({"error": "Payment not found"}), 404

            # Return the payment status
            return jsonify({"status": payment["status"]}), 200
        
        except Exception as e:
            print(f"Error getting payment status: {e}")
            return jsonify({"error": "Error getting payment status"}), 500


    def get_eth_price():
        """Get the lastest ETH price in USD"""

        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        try:
            response = requests.get(url)
            data = response.json()
            return float(data["ethereum"]["usd"])  # Get ETH price in USD
        except Exception as e:
            print(f"Error fetching ETH price: {e}")
            return None
        
    def convert_usd_to_eth(amount):
        """Convert USD to ETH"""
        eth_price = PaymentController.get_eth_price()
        if eth_price is None:
            return None
        return amount / eth_price

    def check_eth_balance(address):
        """Check the ETH balance of an address"""
        balance = w3.eth.get_balance(address)
        return balance



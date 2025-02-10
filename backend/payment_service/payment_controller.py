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

            print(f"amount: {amount}, currency: {currency}, api key: {api_key}")

            # Typecast the amount to a float
            try:
                amount = float(amount)
                print(amount)
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
                print("amount < 0")
                return jsonify({"error": "Invalid amount"}), 400
            
            # Check if the currency is valid
            if currency not in ["ETH"]:
                print("currency not eth")
                return jsonify({"error": "Invalid currency"}), 400

            # Convert the amount to ETH
            eth_amount = PaymentController.convert_usd_to_eth(amount)

            if float(eth_amount) < 0.01:
                return jsonify({"error": "Minimum payment amount is 0.01 ETH"}), 400

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
            total_fee = fee + gas_fee*2
            ### END OF FEE CALCULATION ###

            ### CREATE A PAYMENT OBJECT ###
            payment = PaymentModel(user_id, 
                                   payment_address, 
                                   private_key, 
                                   eth_amount, 
                                   total_fee)
            ### END OF PAYMENT OBJECT CREATION ###

            # Save the payment to the database
            payment.save()

            return jsonify({"payment_address": payment_address, "eth_amount": eth_amount}), 200

        except Exception as e:
            print(f"Error creating payment: {e}")
            return jsonify({f"error": f"Error creating payment: {e}"}), 500


    @staticmethod
    def update_payment_status(data):
        """Update the status of a payment"""
        try:
            ### DATABASE CONNECTION ###
            db_users = Database.get_collection("users")
            ### END OF DATABASE CONNECTION ###

            ### DATA PROCESSING ###
            # Get the API key from the request
            api_key = data.get("api_key")
            user = db_users.find_one({"api_key": api_key})
            if not user:
                return jsonify({"error": "Invalid API key"}), 401
                        
            # Get the payment from the database
            payment_address = data.get("payment_address")
            payment = PaymentModel.find_by_payment_address(payment_address)
            if not payment:
                return jsonify({"error": "Payment not found"}), 404
            ### END OF DATA PROCESSING ###
            
            ### BALANCE CHECK ###
            # Get the balance of the payment address
            balance_eth = PaymentController.check_eth_balance(payment_address)

            if balance_eth > payment["amount"]:
                # Send money back to user wallet and fee to admin wallet
                user_fund = payment["amount"] - payment["fee"]
                admin_fund = payment["fee"]
                admin_wallet = os.getenv("ADMIN_WALLET_ADDRESS")
                user_wallet = user["wallet_address"]
                payment_address_private_key = payment["payment_address_private_key"]
                print(f"User fund: {user_fund}\nAdmin fund: {admin_fund}\nUser wallet: {user_wallet}\nAdmin wallet: {admin_wallet}\nPayment address: {payment_address}\nPayment address private key: {payment_address_private_key}")
                try:
                    user_tx, admin_tx = PaymentController.fund_distribute(
                                                                        user_fund, 
                                                                        admin_fund, 
                                                                        user_wallet, 
                                                                        admin_wallet, 
                                                                        payment_address,
                                                                        payment_address_private_key)


                except Exception as e:
                    print(f"Error distributing funds: {e}")
                    return jsonify({"error": f"Error distributing funds: {e}"}), 500

                # Update the status of the payment
                PaymentModel.update_payment(payment["_id"], {"status": "paid"})

                return jsonify({"status": "Payment paid successfully", "user_tx": user_tx, "admin_tx": admin_tx}), 200
            else:
                return jsonify({"status": "Payment not paid"}), 400
            ### END OF BALANCE CHECK ###
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
            # Get the ETH price in USD
            response = requests.get(url)
            data = response.json()
            return float(data["ethereum"]["usd"])
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

    def fund_distribute(amount, fee, user_wallet, admin_wallet, payment_wallet,payment_wallet_pk):
        """Distribute the fund to the user and the admin"""
        print(f"Distributing funds to {user_wallet} and {admin_wallet}")
        # Send the amount to the user wallet
        user_tx = PaymentController.send_eth(payment_wallet_pk, payment_wallet, user_wallet, amount)
        # Send the fee to the admin wallet
        admin_tx = PaymentController.send_eth(payment_wallet_pk, payment_wallet, admin_wallet, fee)
        return user_tx, admin_tx


    def send_eth(_from_pk, _from, _to, amount):
        """Send ETH to an address"""
        nonce = w3.eth.get_transaction_count(_from, 'pending')
        print(f"Nonce: {nonce}")

        _from = Web3.to_checksum_address(_from)
        _to = Web3.to_checksum_address(_to)

        if not Web3.is_address(_to):
            print(f"Invalid recipient address: {_to}")

        gas_price = w3.eth.gas_price
        gas_limit = 21000
        value = amount - (gas_price * gas_limit)/10**18

        tx = {
            'nonce': nonce,
            'from': _from,
            'to': _to,
            'value': w3.to_wei(value, 'ether'),
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': 11155111

        }

        signed_tx = w3.eth.account.sign_transaction(tx, _from_pk)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return w3.to_hex(tx_hash)
    
    @staticmethod
    def timeout(data):
        """Update the status of a payment"""
        try:
            ### DATABASE CONNECTION ###
            db_users = Database.get_collection("users")
            ### END OF DATABASE CONNECTION ###

            ### DATA PROCESSING ###
            # Get the API key from the request
            api_key = data.get("api_key")
            user = db_users.find_one({"api_key": api_key})
            if not user:
                return jsonify({"error": "Invalid API key"}), 401
                        
            # Get the payment from the database
            payment_address = data.get("payment_address")
            payment = PaymentModel.find_by_payment_address(payment_address)
            if not payment:
                return jsonify({"error": "Payment not found"}), 404
            
            # Get the balance of the payment address
            balance_eth = PaymentController.check_eth_balance(payment_address)

            # Check if the balance is less than the amount
            if balance_eth < payment["amount"]:
                PaymentModel.update_payment(payment["_id"], {"status": "failed"})
                return jsonify({"status": "Payment failed"}), 200
            else:
                return jsonify({"status": "Payment paid successfully"}), 200

        except Exception as e:
            print(f"Error updating payment status: {e}")
            return jsonify({"error": "Error updating payment status"}), 500

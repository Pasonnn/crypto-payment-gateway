from database.db import Database
import datetime
from cryptography.fernet import Fernet
import secrets
from eth_account import Account

class PaymentModel:
    ### FIND PAYMENTS ###
    @staticmethod
    def find_by_user_id(user_id):
        """Find a payment by user id"""
        return Database.get_collection('payments').find_one({"user_id": user_id})

    @staticmethod
    def find_by_id(payment_id):
        """Find a payment by id"""
        return Database.get_collection('payments').find_one({"_id": payment_id})

    @staticmethod
    def find_by_payment_address(payment_address):
        """Find a payment by payment address"""
        return Database.get_collection('payments').find_one({"payment_address": payment_address})

    @staticmethod
    def find_by_currency(currency):
        """Find payments by currency"""
        return Database.get_collection('payments').find({"currency": currency})
    ### END OF FIND PAYMENTS ###

    ### GENERATE PAYMENT ADDRESS ###
    @staticmethod
    def generate_private_key():
        return "0x" + secrets.token_hex(32)

    @staticmethod
    def generate_payment_address(private_key):
        account = Account.from_key(private_key)
        return account.address
    ### END OF GENERATE PAYMENT ADDRESS ###

    ### INIT PAYMENT ###
    def __init__(self, user_id, payment_address, payment_address_private_key, amount, fee, user_tx = "", admin_tx = "",status="pending"):
        self.user_id = user_id
        self.payment_address = payment_address
        self.payment_address_private_key = payment_address_private_key
        self.amount = amount
        self.fee = fee
        self.status = status
        self.user_tx = user_tx
        self.admin_tx = admin_tx

        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
    ### END OF INIT PAYMENT ###

    ### CRUD OPERATIONS ###
    def save(self):
        """Saves the user to MongoDB"""
        payment_data = self.__dict__
        Database.get_collection('payments').insert_one(payment_data)

    @staticmethod
    def update_payment(payment_id, updates):
        payment_collection = Database.get_collection('payments')
        updates["updated_at"] = datetime.datetime.utcnow()
        payment_collection.update_one({"_id": payment_id}, {"$set": updates})

    @staticmethod
    def delete_payment(payment_id):
        payment_collection = Database.get_collection('payments')
        payment_collection.delete_one({"_id": payment_id})
    ### END OF CRUD OPERATIONS ###


from web3 import Web3
from eth_account import Account

# Connect to Infura Ethereum Node
WEB3_PROVIDER = "https://mainnet.infura.io/v3/8567a21c285f436e9e56e62239dec097"
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

def generate_wallet():
    """Generates a new Ethereum wallet"""
    account = w3.eth.account.create()
    return {"address": account.address, "private_key": account.key.hex()}

def get_transaction_status(tx_hash):
    """Fetches transaction status from Ethereum blockchain"""
    try:
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
        return tx_receipt.status  # 1 = success, 0 = failed
    except:
        return "pending"

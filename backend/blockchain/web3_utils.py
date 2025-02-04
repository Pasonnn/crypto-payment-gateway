from web3 import Web3
from eth_account import Account
import requests
import secrets
import time
from dotenv import load_dotenv
import os

# ✅ Load Environment Variables
load_dotenv()

# ✅ Connect to Ethereum Sepolia via Infura
INFURA_URL = os.getenv("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# ✅ Ensure Sepolia Connection is Working
if w3.is_connected():
    print("✅ Connected to Ethereum Sepolia!")
else:
    print("❌ Failed to connect to Ethereum Sepolia!")

# ✅ Set Chain ID for Sepolia Testnet
CHAIN_ID = 11155111  # Ethereum Sepolia Chain ID

# ✅ Generate a new Ethereum wallet
def generate_wallet():
    """Generates a new Ethereum wallet that is compatible with MetaMask"""
    private_key = "0x" + secrets.token_hex(32)  # Generates a random private key
    account = Account.from_key(private_key)  # Creates an Ethereum wallet
    return {"address": account.address, "private_key": private_key}

# ✅ Fetch the latest ETH price in USD
def get_eth_price():
    """Fetch the latest ETH price in USD"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        return float(data["ethereum"]["usd"])  # Get ETH price in USD
    except Exception as e:
        print(f"❌ Error fetching ETH price: {e}")
        return None

# ✅ Convert USD to ETH based on real-time ETH price
def convert_usd_to_eth(pay_amount):
    """Converts USD to ETH based on current ETH price"""
    eth_price = get_eth_price()
    if eth_price is None:
        return None  # Error fetching price
    return round(pay_amount / eth_price, 8)  # Convert USD to ETH (rounded to 8 decimals)

# ✅ Check the ETH balance of an address
def check_eth_balance(payment_address):
    """Checks the ETH balance of a given address"""
    balance_wei = w3.eth.get_balance(payment_address)  # Get balance in Wei
    return w3.from_wei(balance_wei, "ether")  # Convert from Wei to ETH

# ✅ Monitor ETH balance for payment (checks every 10 seconds)
def monitor_eth_payment(payment_address, required_eth, timeout=600):
    """Monitors ETH balance for payment completion within 10 minutes"""
    start_time = time.time()

    while time.time() - start_time < timeout:
        balance_eth = check_eth_balance(payment_address)

        if balance_eth >= required_eth:
            return {"status": "success", "message": "Payment received!"}
        
        print(f"⏳ Waiting for payment... Current balance: {balance_eth} ETH")
        time.sleep(10)  # Wait 10 seconds before checking again

    return {"status": "failed", "message": "Payment timeout after 10 minutes."}

# ✅ Check transaction status on the blockchain
def get_transaction_status(tx_hash):
    """Fetches transaction status from Ethereum Sepolia"""
    try:
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
        return "confirmed" if tx_receipt.status == 1 else "failed"
    except:
        return "pending"

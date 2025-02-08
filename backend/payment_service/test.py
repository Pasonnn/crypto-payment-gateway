from web3 import Web3
import os

def send_eth(_from_pk, _from, _to, amount):
    """Send ETH to an address"""
    nonce = w3.eth.get_transaction_count(_from)
    print(f"Nonce: {nonce}")

    if not Web3.is_address(_to):
        print(f"Invalid recipient address: {_to}")

    tx = {
        'nonce': nonce,
        'from': _from,
        'to': _to,
        'value': w3.to_wei(int(amount), 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei(50, 'gwei'),
        'chainId': 11155111
    }

    signed_tx = w3.eth.account.sign_transaction(tx, _from_pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Tx hash: {tx_hash}")
    return w3.to_hex(tx_hash)

w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_SEPOLIA_URL")))

if not w3.is_connected():
    print("Failed to connect to the Ethereum node.")
else:
    print("Connected to the Ethereum node.")

try:
    admin_private_key = "b3871dd719cfcead5edf6172d641b6d423c2b94e66b65d9632a2fd5b2b28048f"
    admin_address = "0x3f1fc384bd71a64cb031983fac059c9e452ad247"
    recipient_address = "0x36F0C8B1A74be0c623BeAe35ecE1838028C45EFF"
        
    admin_address = Web3.to_checksum_address(admin_address)
    recipient_address = Web3.to_checksum_address(recipient_address)

    amount_to_send = 0.0001  # Amount in ETH


    tx_hash = send_eth(admin_private_key, admin_address, recipient_address.lower(), amount_to_send)
    if tx_hash:
        print(f"Transaction successful with hash: {tx_hash}")
    else:
        print("Transaction failed.")
except Exception as e:
    print(f"An error occurred: {e}")

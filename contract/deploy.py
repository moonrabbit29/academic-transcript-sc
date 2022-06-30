from dotenv import load_dotenv
from solcx import compile_standard
from web3 import Web3
import os
import json
import sys
load_dotenv()

environtment = sys.argv[1] if sys.argv else "development"

if environtment == "development" : 
    # connecting to ganache
    eth_endpoint = os.environ.get('ETHEREUM_ENDPOINT_URI_DEVELOPMENT')
    # private ethereum 
    private_key = os.environ.get("PRIVATE_KEY_DEV")
    # address
    my_address = os.environ.get("ACCOUNT_ADDRESS_DEV")
    chain_id = 1337
else :
    eth_endpoint = os.environ.get('ETHEREUM_ENDPOINT_URI_PROD')
    # private ethereum 
    private_key = os.environ.get("PRIVATE_KEY_PROD")
    # address
    my_address = os.environ.get("ACCOUNT_ADDRESS_PROD")
    chain_id = 4


with open("contract/CertificateSC.sol", "r") as file:
    sertificate_sc_file = file.read()

with open("contract/Authorization.sol", "r") as file:
    authorization_sc_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "CertificateSC.sol": {"content": sertificate_sc_file},
            "Authorization.sol" : {"content" :authorization_sc_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.7",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["CertificateSC.sol"]["CertificateSC"]["evm"][
"bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["CertificateSC.sol"]["CertificateSC"]["metadata"]
)["output"]["abi"]


w3 = Web3(Web3.HTTPProvider(eth_endpoint))

nonce = w3.eth.getTransactionCount(my_address)

CertificateSC = w3.eth.contract(abi=abi, bytecode=bytecode)

transaction = CertificateSC.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Sign the transaction
# store transaction 4:16:43
print(f"private key {private_key}")
signed_txn = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)

# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

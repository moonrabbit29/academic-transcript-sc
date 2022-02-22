from web3 import Web3
import json


class Web3Helper:
    def __init__(self, app):
        self.w3 = Web3(Web3.HTTPProvider(
            app.config.get('ETHEREUM_ENDPOINT_URI')))
        self.abi = self.__init_abi_data()
        self.contract_address = app.config.get('SMART_CONTRACT_ADDRESS')
        self.my_address = app.config.get('ACCOUNT')
        self.nonce = self.w3.eth.getTransactionCount(self.my_address)
        self.chain_id = app.config.get('CHAIN_ID')
        self.counter = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)
        self.private_key = app.config.get('ACCOUNT_KEY')
        print(
            f" Contract address : {self.contract_address} \n Chain ID : {self.chain_id}")

    def __init_abi_data(self):
        with open('compiled_code.json') as f:
            data = json.load(f)
        abi = abi = json.loads(
            data["contracts"]["CertificateSC.sol"]["CertificateSC"]["metadata"])["output"]["abi"]
        return abi

    def issuing_transcript(self, tc_hash, student_hash):
        register_tc_tx = self.counter.functions.register_transcript(tc_hash, student_hash).buildTransaction(
            {
                "chainId": self.chain_id, "gasPrice": self.w3.eth.gas_price, "from": self.my_address, "nonce": self.nonce
            }
        )
        signed_register_txn = self.w3.eth.account.sign_transaction(
            register_tc_tx, private_key=self.private_key)
        send_register_tx = self.w3.eth.send_raw_transaction(
            signed_register_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(send_register_tx)
        retVal = self.w3.eth.getTransactionReceipt(
            tx_receipt['transactionHash'])['logs'][0]['data']
        print(f"retVal => {retVal}")
        return "testing aja"

    def retrieve_transcript(self, student_hash):
        student_tc = self.counter.functions.retrieve_student_transcript(
            student_hash).call()
        print(f"retVal => {student_tc}")
        return "testing aja"

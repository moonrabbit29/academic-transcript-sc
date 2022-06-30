from web3 import Web3
import json
from app.helper.hash import Hash
from datetime import datetime


class Web3Helper(Hash):

    def __simplified(self, tuple):
        ts = datetime.utcfromtimestamp(tuple[1]).strftime('%Y-%m-%d %H:%M:%S')
        return {"data_hash": tuple[0], "timestamp": ts}

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
        self.nonce = self.w3.eth.getTransactionCount(self.my_address)
        register_tc_tx = self.counter.functions.register_transcript(tc_hash, student_hash).buildTransaction(
            {
                "chainId": self.chain_id, "gasPrice": self.w3.eth.gas_price, "from": self.my_address, "nonce": self.nonce
            }
        )
        signed_register_txn = self.w3.eth.account.sign_transaction(
            register_tc_tx, private_key=self.private_key)
        try:
            send_register_tx = self.w3.eth.send_raw_transaction(
                signed_register_txn.rawTransaction)
        except Exception as ex:
            return {"status": 500, "data": {}, "message": f"Failed to transact with the SC. This {ex} is causing the error"}
        try:
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(
                send_register_tx, timeout=120)
        except Web3.exceptions.TimeExhausted:
            return {"status": 500, "data": {}, "message": "Couldn't get transaction receipt timeout"}
        except Exception as ex:
            return {"status": 500, "data": {}, "message": f"Couldn't get transaction receipt. This {ex} causing an error"}
        print(tx_receipt['status'])
        is_file_not_present = int(tx_receipt['logs'][0]['data'][2:])
        transaction_hash = tx_receipt["transactionHash"].hex()
        block_hash = tx_receipt["blockHash"].hex()
        if(is_file_not_present and tx_receipt['status']):
            self.nonce = self.w3.eth.getTransactionCount(self.my_address)
            return {"status": 200, "data": {"tx_hash": transaction_hash, "block_hash": block_hash}, "message": "SUCCESS"}
        elif (not is_file_not_present):
            self.nonce = self.w3.eth.getTransactionCount(self.my_address)
            return {"status": 400, "data": {"tx_hash": transaction_hash, "block_hash": block_hash}, "message": "Data already in blockchain"}
        return {"status": 403, "data": {}, "message": "Transaction failed, failed to add transcript to blockchain"}

    def retrieve_transcript(self, student_hash):
        try:
            student_tc_raw = self.counter.functions.retrieve_student_transcript(
                student_hash).call()
        except Exception as ex:
            return {"status": 500, "data": {}, "message": f"Couldn't get transaction to be done. This {ex} causing an error"}

        student_tc = list(map(self.__simplified, student_tc_raw))
        return {"status": 200, "data": student_tc, "message": "SUCCESS"}

    def verify_transcript(self, tc_hash, student_hash,student_id):
        student_tc = self.counter.functions.verify_certificate_transcript(
            tc_hash,student_hash).call()
        return {"status":200 if student_tc else 400,"data":student_tc,"message":f"certificate valid own by {student_id}"
                if student_tc else "certificate not valid"}

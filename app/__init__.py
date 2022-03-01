#from crypt import methods
from unittest import result
from flask import Flask, request, jsonify, send_file
from web3 import Web3
from flask_cors import CORS, cross_origin
from app.web3_helper import Web3Helper
import os

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
cors = CORS(app)

web3helper = Web3Helper(app)


@app.route("/api/issuing-transcript", methods=['POST'])
@cross_origin()
def issuing():
    data = request.get_json()
    result = web3helper.issuing_transcript(
        data['tc_hash'], data['student_hash'])
    return f"The configured secret key is Yahaloo."


@app.route("/api/retrieve-transcript", methods=['POST'])
@cross_origin()
def retrieve():
    data = request.get_json()
    result = web3helper.retrieve_transcript(
        data['student_hash'])
    return f"The configured secret key is Yahaloo."

#app route verify method post
@app.route("/api/verifying-transcript", methods=['POST'])
@cross_origin()
def verifying():
    data = request.get_json()
    result = web3helper.verify_transcript(
        data['student_hash'], data['tc_hash'])
    return f"The configured secret key is Yahaloo."
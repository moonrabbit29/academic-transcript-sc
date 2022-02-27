from flask import Flask, request, jsonify, send_file
from web3 import Web3
from flask_cors import CORS, cross_origin
from app.helper.web3_helper import Web3Helper
import os

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
cors = CORS(app)

web3helper = Web3Helper(app)


@app.route("/api/issuing-transcript", methods=['POST'])
@cross_origin()
def issuing():
    try:
        data = request.get_json()
        # temporary
        # TODO : convert data into pdf file
        # TODO : store metadata in database
        student_number, tc_data = data['student_identity']['nim'], f"{data['score']}"
        student_num_hash, tc_hash = web3helper.hash_data(
            student_number.encode()), web3helper.hash_data(tc_data.encode())
    except Exception as ex:
        print(ex)
    result = web3helper.issuing_transcript(
        tc_hash, student_num_hash)
    return jsonify(result), result["status"]


@app.route("/api/retrieve-transcript", methods=['POST'])
@cross_origin()
def retrieve():
    data = request.get_json()
    result = web3helper.retrieve_transcript(
        data['student_hash'])
    return jsonify(result), result["status"]

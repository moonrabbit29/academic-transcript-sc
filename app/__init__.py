from typing import List
from flask import Flask, request, jsonify, send_file,make_response
from web3 import Web3
from flask_cors import CORS, cross_origin
from app.helper.web3_helper import Web3Helper
from app.helper.document_helper import DocumentHelper
import os
import ipfshttpclient
import json

app = Flask(__name__,template_folder='public/templates')
app.config.from_object(os.environ.get('APP_SETTINGS'))
cors = CORS(app)
ipfsClient = ipfshttpclient.connect()

web3helper = Web3Helper(app)
documentHelper = DocumentHelper(app)

#app route issuing transcript
@app.route("/api/issuing-transcript", methods=['POST'])
@cross_origin()
def issuing():
    try:
        data = request.get_json()
        student_number, tc_data = data['student_identity']['nim'], data
        tc_document,document_status_failed = documentHelper.generate_document(tc_data)
        if document_status_failed :
            return 500,jsonify({"Error : Failed to generate transcript document"})
        #tc_document_bytes =tc_document.getvalue()
        with open("transcript_data.json", "w") as file:
            json.dump(tc_data, file)
        with open("transcript_data.json", "rb") as file:
            tc_hash_result = ipfsClient.add(file)
        student_num_hash, tc_hash = web3helper.hash_data(
            student_number.encode()),tc_hash_result['Hash']
    except Exception as ex:
        return 500,jsonify({"Error" : str(ex)})
    result = web3helper.issuing_transcript(
        tc_hash, student_num_hash)
    if(result['status'] != 200) :
        return jsonify(result),result['status']
    response = make_response(send_file(tc_document,
            as_attachment=True,mimetype='application/pdf',attachment_filename="result.pdf"))
    response.headers['result'] = result
    return response

#app route retrieve transcript
@app.route("/api/retrieve-transcript", methods=['POST'])
@cross_origin()
def retrieve():
    data = request.get_json()
    student_hash = web3helper.hash_data(
            data['student_id'].encode())
    print(f"student hash -> {student_hash}")
    result = web3helper.retrieve_transcript(
        student_hash)
    return jsonify(result), result["status"]

#app route verify method post
@app.route("/api/verifying-transcript", methods=['POST'])
@cross_origin()
def verifying():
    data = request.get_json()
    student_id_hash = web3helper.hash_data(
            data['student_id'].encode())
    with open("transcript_data.json", "w") as file:
            json.dump(data['tc_data'], file)
    with open("transcript_data.json", "rb") as file:
            tc_hash_result = ipfsClient.add(file)
    result = web3helper.verify_transcript(
        tc_hash_result['Hash'], student_id_hash, data['student_id'])
    return jsonify(result),result["status"]

#app route get data from ipfs


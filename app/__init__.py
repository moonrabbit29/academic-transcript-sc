from flask import Flask, request, jsonify, send_file,make_response, render_template
from web3 import Web3
from flask_cors import CORS, cross_origin
from app.helper.web3_helper import Web3Helper
from app.helper.document_helper import DocumentHelper
import os

app = Flask(__name__,template_folder='public/templates')
app.config.from_object(os.environ.get('APP_SETTINGS'))
cors = CORS(app)

web3helper = Web3Helper(app)
documentHelper = DocumentHelper(app)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/index.html')
def dashboard():
    return render_template('index.html')
@app.route('/register.html')
def register():
    return render_template('register.html')
@app.route('/retrieve.html')
def get():
    return render_template('retrieve.html')
@app.route('/verify.html')
def cek():
    return render_template('verify.html')

@app.route("/api/issuing-transcript", methods=['POST'])
@cross_origin()
def issuing():
    try:
        data = request.get_json()
        # temporary
        # TODO : store metadata in database
        student_number, tc_data = data['student_identity']['nim'], data
        tc_document,document_status_failed = documentHelper.generate_document(tc_data)
        if document_status_failed : 
            return 500,jsonify({"Error : Failed to generate transcript document"})
        tc_document_bytes =tc_document.getvalue()
        student_num_hash, tc_hash = web3helper.hash_data(
            student_number.encode()),web3helper.hash_data(tc_document_bytes)
        print(f"tc hash {tc_hash}")
    except Exception as ex:
        print("ERROR")
        return 500,jsonify({"Error" : str(ex)})
    result = web3helper.issuing_transcript(
        tc_hash, student_num_hash)
    response = make_response(send_file(tc_document,
            as_attachment=True,mimetype='application/pdf',attachment_filename="result.pdf"))
    response.headers['result'] = result
    return response


@app.route("/api/retrieve-transcript", methods=['POST'])
@cross_origin()
def retrieve():
    data = request.get_json()
    result = web3helper.retrieve_transcript(
        data['student_hash'])
    return jsonify(result), result["status"]

#app route verify method post
@app.route("/api/verifying-transcript", methods=['POST'])
@cross_origin()
def verifying():
    data = request.get_json()
    result = web3helper.verify_transcript(
        data['student_hash'], data['tc_hash'])
    return f"The configured secret key is Yahaloo."

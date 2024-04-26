from flask import Flask, request
from flask_cors import CORS
# from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/summarizeFile", methods=["POST"])
def summarizeFile():
    file = request.files['file']
    print(file)
    return "File received"

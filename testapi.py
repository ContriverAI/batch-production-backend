from flask import Flask, url_for, request, render_template, jsonify
import threading
import pandas as pd
import data_storage
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/get/users', methods = ['GET', 'POST'])
def getusers():
    data = request.json
    print(data['username'])
    return 'done'

app.run(host='0.0.0.0', port=9001)

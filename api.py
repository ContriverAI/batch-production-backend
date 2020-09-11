from flask import Flask, url_for, request, render_template, jsonify
import threading
import pandas as pd
import data_storage
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get/users', methods = ['GET', 'POST'])
def getusers():
    data = request.json
    username = data['username']
    username = username.lower()
    username = username.capitalize()
    passw = data['password']
    users = data_storage.get_users()
    try:
        try:
            role = users.loc[(users['username']==username) & (users['passwords']==passw),'role'].iloc[0]
            designation = users.loc[(users['username']==username) & (users['passwords']==passw),'designation'].iloc[0]
        except:
            pass
        if len(users[(users['username']==username) & (users['passwords'] == passw)])>0:
            a = {
                "username" : username,
                "designation":designation,
                "role":role
            }
            return jsonify(a)
        else:
            a = {"msg":"Invalid Creds..!"}
            return jsonify(a)
    except:
        a = {"msg":"Something Went Wrong..!"}
        return jsonify(a)

@app.route('/get/cooling_data', methods = ['GET', 'POST'])
def getcoolingdata():
    data = request.json
    coolingdata = data_storage.cooling()
    coolingdata = coolingdata.to_json(orient="split")
    return jsonify(coolingdata)

app.run(host='0.0.0.0', port=9001)

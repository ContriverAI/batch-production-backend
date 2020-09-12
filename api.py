from flask import Flask, url_for, request, render_template, jsonify
import threading
import pandas as pd
import data_storage
from flask_cors import CORS
import uuid
import json

app = Flask(__name__)
CORS(app)

@app.route('/get/users', methods = ['GET', 'POST'])
def getusers():
    data = request.json
    username = data['username']
    username = username.lower()
    passw = data['password']
    users = data_storage.get_users()
    try:
        try:
            role = users.loc[(users['username']==username) & (users['passwords']==passw),'role'].iloc[0]
            designation = users.loc[(users['username']==username) & (users['passwords']==passw),'designation'].iloc[0]
            u_key = users.loc[(users['username']==username) & (users['passwords']==passw),'u_key'].iloc[0]
        except:
            pass
        if len(users[(users['username']==username) & (users['passwords'] == passw)])>0:
            a = {
                "username" : username,
                "designation" : designation,
                "role" : role,
                "u_key" : u_key
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
    coolingdata = json.loads(coolingdata)
    coolingdata = json.dumps(coolingdata)
    return coolingdata

@app.route('/get/create_user', methods = ['GET', 'POST'])
def createuser():
    data = request.json
    username = data['username']
    password = data['password']
    designation = data['designation']
    role = data['role']
    all_ukey = data_storage.u_key()
    ids = uuid.uuid1()
    ids = str(ids)
    token = True
    while token:
        if ids in all_ukey:
            ids = uuid.uuid1()
            ids = str(ids)
        else:
            token = False
    user = data_storage.create_user(username,password,designation,role,ids)
    return user

@app.route('/get/update_user', methods = ['GET', 'POST'])
def updateuser():
    data = request.json
    username = data['username']
    password = data['password']
    designation = data['designation']
    role = data['role']
    user = data_storage.update_user(username,password,designation,role)
    return user

@app.route('/get/delete_user', methods = ['GET', 'POST'])
def deleteuser():
    data = request.json
    u_key = data['username']
    user = data_storage.delete_user(u_key)
    return user

@app.route('/get/allusers', methods = ['GET', 'POST'])
def allusers():
    data = data_storage.get_users()
    data = data.to_json(orient="split")
    data = json.loads(data)
    data = json.dumps(data)
    return data

app.run(host='0.0.0.0', port=9002)
from flask import Flask, url_for, request, render_template, jsonify
import threading
import pandas as pd
import data_storage
from flask_cors import CORS
import uuid
import json
from flask_socketio import SocketIO, emit, disconnect
import socket
from threading import Lock, Timer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
async_mode = "threading"
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")
thread = None
thread_lock = Lock()

def getcoolingdata(socketio):
    coolingdata = data_storage.cooling()
    coolingdata = coolingdata.to_json(orient="split")
    coolingdata = json.loads(coolingdata)
    coolingdata = json.dumps(coolingdata)
    socketio.emit('data',coolingdata)

def bg_thread_cooling_data():
    while True:
        getcoolingdata(socketio)

@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(bg_thread_cooling_data)
    emit('conn', {'data': 'Connected'})

@app.route('/', methods = ['GET', 'POST'])
def y():
    return render_template('sample.html')

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

@app.route('/get/create_cooling_main', methods = ['GET', 'POST'])
def createcoolingmain():
    data = request.json
    print(data)
    confsdata = data_storage.configparams()
    print(confsdata)
    date = data['date']
    trolley = data['trolleyNo']
    product = data['product']
    shftnumber = data['shiftProduced']
    quant = data['quantity']
    timein = data['coolingTime']
    u_key = data['u_key']
    duration = confsdata.loc[(confsdata['productcode']==product),'duration'].iloc[0]
    completetime = duration + timein
    completetime = str(completetime).split()
    completetime = completetime[2]
    duration = str(duration).split()
    duration = duration[2]
    updatedata = data_storage.create_cooling_main(date,trolley,product,shftnumber,quant,timein,u_key,duration,completetime)
    return updatedata

@app.route('/get/create_cooling_packaging', methods = ['GET', 'POST'])
def createcoolingpackaging():
    data = request.json
    print(data)
    u_key = data['u_key']
    trolley = data['trolleyNo']
    status = data['status']
    time = data['time']
    updatedata = data_storage.create_cooling_packaging(u_key,trolley,status,time)
    return updatedata

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

@app.route('/get/configparams', methods = ['GET', 'POST'])
def configparams():
    data = data_storage.configparams()
    data = data.to_json(orient="split")
    data = json.loads(data)
    data = json.dumps(data)
    return data

@app.route('/get/updateconfigparams', methods = ['GET', 'POST'])
def updateconfigparams():
    data = request.json
    productname = data['productName']
    productcode = data['productCode']
    duration = data['duration']
    updateconfig = data_storage.updateconfig(productname,productcode,duration)
    return updateconfig

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=9001)

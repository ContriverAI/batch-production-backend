from flask import Flask, url_for, request, render_template, jsonify
import threading
import pandas as pd
import data_storage
import uuid
import json
from flask_socketio import SocketIO, emit, disconnect
import socket
from threading import Lock, Timer
import time
from flask_cors import CORS, cross_origin
import logical_data_update

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
async_mode = "threading"
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")
thread = None
thread_lock = Lock()
CORS(app, support_credentials=True)

def getcoolingdata(socketio):
    coolingdata = data_storage.cooling()
    coolingdata = coolingdata.to_json(orient="split")
    coolingdata = json.loads(coolingdata)
    coolingdata = json.dumps(coolingdata)
    proddata = data_storage.production_data()
    proddata = proddata.to_json(orient="split")
    proddata = json.loads(proddata)
    proddata = json.dumps(proddata)
    storedata = data_storage.store_data()
    storedata = storedata.to_json(orient="split")
    storedata = json.loads(storedata)
    storedata = json.dumps(storedata)
    data = {
        "cooling":coolingdata,
        "proddata":proddata,
        "store":storedata
    }
    socketio.emit('data',data)

def bg_thread_cooling_data():
    while True:
        getcoolingdata(socketio)

@socketio.on('connect')
@cross_origin(supports_credentials=True)
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(bg_thread_cooling_data)
    emit('conn', {'data': 'Connected'})
    return "emitted"

@app.route('/', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def y():
    return render_template('sample.html')

@app.route('/get/users', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
def updateuser():
    data = request.json
    username = data['username']
    password = data['password']
    designation = data['designation']
    role = data['role']
    user = data_storage.update_user(username,password,designation,role)
    return user

@app.route('/get/delete_user', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def deleteuser():
    data = request.json
    u_key = data['username']
    user = data_storage.delete_user(u_key)
    return user

@app.route('/get/allusers', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def allusers():
    data = data_storage.get_users()
    data = data.to_json(orient="split")
    data = json.loads(data)
    data = json.dumps(data)
    return data

@app.route('/get/configparams', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def configparams():
    data = data_storage.configparams()
    data = data.to_json(orient="split")
    data = json.loads(data)
    data = json.dumps(data)
    return data

@app.route('/get/updateconfigparams', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def updateconfigparams():
    data = request.json
    productname = data['productName']
    productcode = data['productCode']
    duration = data['duration']
    updateconfig = data_storage.updateconfig(productname,productcode,duration)
    return updateconfig

@app.route('/get/productiondata', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def productiondata():
    data = data_storage.production_data()
    data = data.to_json(orient="split")
    data = json.loads(data)
    data = json.dumps(data)
    return data

@app.route('/get/storedata', methods = ['GET', 'POST'])
def storedata():
    data = data_storage.store_data()
    data = data.to_json(orient="split")
    data = json.loads(data)
    data = json.dumps(data)
    return data

@app.route('/get/production_main_screen', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def prodmainscreen():
    data = request.json
    Date = data['date']
    Batch = data['batch']
    YEAST = data['yeast']
    FLOUR = data['flour']
    Yield_val = data['yield_val']
    SHIFT = data['shift']
    PRODUCT = data['product']
    REMIX = data['remix']
    Time = data['time']
    u_key = data['u_key']
    prodmain = data_storage.prod_main_Screen(Date,Batch,YEAST,FLOUR,u_key,Yield_val,SHIFT,PRODUCT,REMIX,Time,PRODUCT)
    return prodmain

@app.route('/get/production_recall_screen', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def prodcutionrecallscreen():
    data = request.json
    batch = data['batch']
    time = data['time']
    cancel = data['cancel']
    u_key = data['u_key']
    recallscreen = data_storage.prod_recall_screen(batch,time,cancel,u_key)
    return recallscreen

@app.route('/get/production_bake_screen', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def prodbakescreen():
    data = request.json
    batch = data['batch']
    status = data['status']
    time = data['time']
    u_key = data['u_key']
    bakescreen = data_storage.bakescreen(batch,status,time,u_key)
    return bakescreen

@app.route('/get/store_receiving_screen', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def storereceivingscreen():
    data = request.json
    date = data['date']
    product = data['product']
    St_qty_recv = data['standard_qty_recv']
    rough_qty_recv = data['rough_qty_recv']
    pkg_supervisor = data['supervisor']
    u_key = data['u_key']
    rcscreen = data_storage.storereceivingscreen(date,product,St_qty_recv,rough_qty_recv,pkg_supervisor,u_key)
    return rcscreen

@app.route('/get/store_dispatch_screen', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def storedispatchscreen():
    data = request.json
    date = data['date']
    product = data['product']
    std_dispatched = data['std_dispatched']
    rough_dispatched = data['rough_dispatched']
    rough_returned = data['rough_returned']
    dsp_supervisor = data['dsp_supervisor']
    u_key = data['u_key']
    storedspscreen = data_storage.store_dispatched_screen(date,product,std_dispatched,rough_dispatched,rough_returned,dsp_supervisor,u_key)
    return storedspscreen

if __name__ == '__main__':
    y = threading.Thread(target=logical_data_update.cooling_update)
    y.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=9003)
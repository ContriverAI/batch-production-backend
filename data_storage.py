from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")

def get_users():
    users = pd.read_sql("select * from users;", engine)
    return users

def cooling():
    data = pd.read_sql("select * from Cooling;", engine)
    return data

def create_cooling_main(date,trolley,product,shftprod,quant,timein,u_key,duration,completetime):
    #try:
    query = "select * from cooling;"
    df = pd.read_sql(query,engine)
    index_num = list(np.where((df['trolley']==trolley))[0])
    if len(index_num)>0:
        return 'Trolley Already Exists'
    else:
        query = "insert into Cooling values('"+date+"','"+str(trolley)+"','"+product+"','"+str(quant)+"','"+str(timein)+"','"+str(duration)+"','"+completetime+"','No','"+u_key+"','"+str(shftprod)+"','Not Done');"
        with engine.begin() as conn:
            conn.execute(query)
        return "Record Added Successfully..!"
    #except:
    #    return "Something Went Wrong..!"

def create_cooling_packaging(u_key,trolley,status,time):
    try:
        query = "update Cooling set `packaging complete` = '"+status+"', `complete time` = '"+time+"' where u_key = '"+u_key+"' and trolley = '"+str(trolley)+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Record Added Successfully..!"
    except:
        return "Something Went Wrong..!"
        
def u_key():
    data = pd.read_sql("select u_key from users;", engine)
    return data

def create_user(username,password,designation,role,ids):
    query = "select * from users;"
    df = pd.read_sql(query,engine)
    index_num = list(np.where((df['username']==username))[0])
    if len(index_num)>0:
        return 'User Already Exists'
    else:
        query = "insert into users values('"+username+"','"+password+"','"+designation+"','"+role+"','"+ids+"');"
        with engine.begin() as conn:
            conn.execute(query)
        return 'New User Added'
    return "Something Went Wrong..!"

def update_user(username,password,designation,role):
    query = "select * from users;"
    df = pd.read_sql(query,engine)
    index_num = list(np.where((df['username']==username))[0])
    if len(index_num)>0:
        query = "UPDATE users SET passwords = '"+password+"', role = '"+role+"', designation = '"+designation+"' where username = '"+username+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return 'Successfully Updated User'    
    else:
        return 'User Does Not Exist'

def delete_user(u_key):
    df = pd.read_sql("select * from users;",engine)
    if(len(df.loc[df['username']==u_key])):
        query = "Delete from users where username='"+u_key+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Successfully Deleted Record"
    else:
        return "Record Doesn't Exist"

def configparams():
    query = "select * from configparams;"
    data = pd.read_sql(query, engine)
    return data

def updateconfig(productname,productcode,duration):
    try:
        query = "update configparams set productname = '"+productname+"', duration = '"+duration+"' where productcode = '"+productcode+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Successfully Updated Duration"
    except:
        return  "Something Went Wrong..!"

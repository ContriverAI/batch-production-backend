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
    query = "select * from Cooling;"
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

def production_data():
    query = "select * from Production;"
    data = pd.read_sql(query, engine)
    return data

def store_data():
    query = "select * from store;"
    data = pd.read_sql(query, engine)
    return data

def prod_main_Screen(Date,Batch,YEAST,FLOUR,Yield,u_key,Yield_val,SHIFT,PRODUCT,REMIX,WaterUsed,Time):
    try:
        query = "insert into Production values('"+Date+"','"+FLOUR+"','"+SHIFT+"','"+REMIX+"','"+YEAST+"',' ',' ',' ',' ',' ','"+Time+"',' ','"+u_key+"','"+Batch+"',' ','"+Yield_val+"',' ',' ');"
        with engine.begin() as conn:
            conn.execute(query)
        query = "update Production set '"+Yield+"' = '"+Yield_val+"' where `Mixing Time` = '"+Time+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Successfully Record Added"
    except:
        return "Something Went Wrong"

def prod_recall_screen(batch,time,cancel,u_key):
    try:
        query = "update Production set `recall time` = '"+time+"', `batch recall` = '"+cancel+"' where batch = '"+batch+"' and u_key = '"+u_key+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Updated Successfully"
    except:
        return "Something Went Wrong"

def bakescreen(batch,status,time,u_key):
    try:
        query = "update Production set `Baking Time` = '"+time+"', status = '"+status+"' where batch = '"+batch+"' and u_key = '"+u_key+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Updated Successfully"
    except:
        return "Something Went Wrong"

def storereceivingscreen(date,product,St_qty_recv,rough_qty_recv,pkg_supervisor,u_key):
    try:
        query = "insert into store values('"+date+"','"+product+"','"+St_qty_recv+"','"+rough_qty_recv+"',' ',' ',' ',' ',' ','"+u_key+"','"+pkg_supervisor+"',' ');"
        with engine.begin() as conn:
            conn.execute(query)
        return "Record Added Successfully"
    except:
        return "Something Went Wrong"

def store_dispatched_screen(date,product,std_dispatched,rough_dispatched,rough_returned,dsp_supervisor,u_key):
    try:
        query = "update store set 'dispatched_date' = '"+date+"', `dispatched standard` = '"+std_dispatched+"', `dispatched rough` = '"+rough_dispatched+"', `rough returned` = '"+rough_returned+"', `dsp_supervisor` = '"+dsp_supervisor+"' where product = '"+product+"' and u_key = '"+u_key+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Updated Successfully"
    except:
        return "Something Went Wrong"
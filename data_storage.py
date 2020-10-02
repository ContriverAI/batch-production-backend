from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from datetime import datetime
import sys

def convert_to_date(date):
    new_date = str(datetime.strptime(date,"%d-%m-%Y").date())
    return new_date

engine = create_engine("mysql+pymysql://testuser:CFB98765@localhost/batch?host=localhost")

def get_users():
    users = pd.read_sql("select * from users;", engine)
    return users

def cooling():
    data = pd.read_sql("select * from cooling where date_time = curdate() order by `remaining time` asc;", engine)
    return data

def create_cooling_main(date,trolley,product,shftprod,quant,timein,u_key,duration,completetime):
    try:
        query = "select * from cooling where date_time = curdate();;"
        df = pd.read_sql(query,engine)
        index_num = list(np.where(((df['trolley']==int(trolley))&(df['shift number']==shftprod)))[0])
        if len(index_num)>0:
            return 'Trolley Already Exists'
        else:
            query = "insert into cooling values('"+convert_to_date(date)+"','"+str(trolley)+"','"+product+"','"+str(quant)+"','"+str(timein)+"','"+str(duration)+"','"+completetime+"','No','"+u_key+"','"+str(shftprod)+"','Not Done','00:00:00');"
            print(query)
            with engine.begin() as conn:
                conn.execute(query)
            return "Record Added Successfully..!"
    except:
        sys.exit()

def create_cooling_packaging(u_key,trolley,status,time):
    # try:
    query = "update cooling set `packaging complete` = '"+status+"', `complete time` = '"+time+"', u_key = '"+u_key+"' where trolley = "+str(trolley)+" and date_time = curdate();"
    print(query)
    with engine.begin() as conn:
        conn.execute(query)
    return "Record Updated Successfully..!"
    # except:
        # return "Something Went Wrong..!"
        
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

def updateconfig(productcode,duration):
    try:
        query = "update configparams set duration = '"+duration+"' where productcode = '"+productcode+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Successfully Updated Duration"
    except:
        return  "Something Went Wrong..!"

def production_data():
    query = "select * from production where date_time = curdate();;"
    data = pd.read_sql(query, engine)
    return data

def store_data():
    query = "select * from store where date_time = curdate();;"
    data = pd.read_sql(query, engine)
    return data 

def prod_main_Screen(Date,Batch,YEAST,FLOUR,u_key,Yield_val,SHIFT,PRODUCT,REMIX,Time,product):
    query = "select * from production where date_time = curdate();"
    df = pd.read_sql(query, engine)
    index_num = list(np.where(((df['batch']==str(Batch))&(df['shift'] == str(SHIFT))&(df['status']=='Unbaked')))[0])
    if len(index_num)>0:
            return "Batch & Shift Already Exists With Unbaked Status..!"
    else:
        query = "insert into production values('"+convert_to_date(Date)+"','"+str(FLOUR)+"','"+str(SHIFT)+"','"+str(REMIX)+"','"+str(YEAST)+"','"+str(Time)+"',' ','"+str(u_key)+"','"+str(Batch)+"','Unbaked','"+str(Yield_val)+"','No',' ','"+product+"');"
        with engine.begin() as conn:
            conn.execute(query)
        return "Successfully Record Added"

def prod_recall_screen(batch,time,cancel,u_key):
    try:
        query = "update production set `recall time` = '"+str(time)+"', `batch recall` = '"+str(cancel)+"', u_key = '"+str(u_key)+"' where batch = '"+str(batch)+"' and date_time = curdate();"
        with engine.begin() as conn:
            conn.execute(query)
        return "Updated Successfully"
    except:
        return "Something Went Wrong"

def bakescreen(batch,status,time,u_key):
    try:
        query = "update production set `Baking Time` = '"+str(time)+"', status = '"+str(status)+"', u_key = '"+str(u_key)+"' where batch = "+str(batch)+" and date_time = curdate();"
        with engine.begin() as conn:
            conn.execute(query)
        return "Successfully Updated Batch"
    except:
        return "Something Went Wrong"

def storereceivingscreen(date,product,St_qty_recv,rough_qty_recv,pkg_supervisor,u_key):
    try:
        query = "insert into store values('"+convert_to_date(date)+"','"+str(product)+"','"+str(St_qty_recv)+"','"+str(rough_qty_recv)+"','0','0','0','0','0','"+str(u_key)+"','"+str(pkg_supervisor)+"','"+date+"',' ');"
        with engine.begin() as conn:
            conn.execute(query)
        return "Record Added Successfully"
    except:
        return "Something Went Wrong"

def store_dispatched_screen(date,product,std_dispatched,rough_dispatched,rough_returned,dsp_supervisor,u_key):
    try:
        query = "update store set dispatched_date = '"+convert_to_date(date)+"', `dispatched standard` = '"+str(std_dispatched)+"', `dispatched rough` = '"+str(rough_dispatched)+"', `rough returned bread` = '"+str(rough_returned)+"', `dsp_supervisor` = '"+str(dsp_supervisor)+"' where product = '"+str(product)+"' and date_time = curdate();"
        with engine.begin() as conn:
            conn.execute(query)
        return "Updated Successfully"
    except:
        return "Something Went Wrong"

def coolingreport(dateto,datefrom,product,pkgcomplete):
    query = "select `date_time`,product,sum(qty),`packaging complete` from cooling group by `date_time`,product,`packaging complete` having (`date_time` between '"+datefrom+"' and '"+dateto+"') and `packaging complete` in "+str(tuple(pkgcomplete))+" and product in "+str(tuple(product))+";"
    df = pd.read_sql(query, engine)
    return df

def coolingreportp1pk1(dateto,datefrom,product,pkgcomplete):
    query = "select `date_time`,product,sum(qty),`packaging complete` from cooling group by `date_time`,product,`packaging complete` having (`date_time` between '"+datefrom+"' and '"+dateto+"') and `packaging complete` ='"+pkgcomplete+"' and product = '"+product+"';"
    df = pd.read_sql(query, engine)
    return df

def coolingreportp0pk1(dateto,datefrom,product,pkgcomplete):
    query = "select `date_time`,product,sum(qty),`packaging complete` from cooling group by `date_time`,product,`packaging complete` having (`date_time` between '"+datefrom+"' and '"+dateto+"') and `packaging complete` in ('"+str(pkgcomplete)+"') and product in "+str(tuple(product))+";"
    df = pd.read_sql(query, engine)
    return df

def coolingreportp1pk0(dateto,datefrom,product,pkgcomplete):
    query = "select `date_time`,product,sum(qty),`packaging complete` from cooling group by `date_time`,product,`packaging complete` having (`date_time` between '"+datefrom+"' and '"+dateto+"') and `packaging complete` in "+str(tuple(pkgcomplete))+" and product = '"+product+"';"
    df = pd.read_sql(query, engine)
    return df

def storereport(dateto,datefrom,product):
    query = "select date_time,product,sum(`qty received standard`),sum(`qty received rough`), sum(`dispatched standard`), sum(`dispatched rough`), sum(`rough returned bread`), sum(`bread in store`), sum(`rough bread in store`), pkg_supervisor, dsp_supervisor from store group by date_time,product,pkg_supervisor,dsp_supervisor having (date_time between '"+datefrom+"' and '"+dateto+"') and product in "+str(tuple(product))+";"
    df = pd.read_sql(query, engine)
    return df

def storereportp1(dateto,datefrom,product):
    query = "select date_time,product,sum(`qty received standard`),sum(`qty received rough`), sum(`dispatched standard`), sum(`dispatched rough`), sum(`rough returned bread`), sum(`bread in store`), sum(`rough bread in store`), pkg_supervisor, dsp_supervisor from store group by date_time,product,pkg_supervisor,dsp_supervisor having (date_time between '"+datefrom+"' and '"+dateto+"') and product = '"+product+"';"
    df = pd.read_sql(query, engine)
    return df

def prodreport(dateto,datefrom,status,product):
    query = "select date_time, product, shift, batch, sum(flour), sum(remix), sum(yeast), sum(yield), status, `batch recall` from production group by date_time, product, shift, batch, status, `batch recall` having (date_time between '"+datefrom+"' and '"+dateto+"') and status in "+str(tuple(status))+" and product in "+str(tuple(product))+";"
    df = pd.read_sql(query, engine)
    return df

def prodreports0p1(dateto,datefrom,status,product):
    query = "select date_time, product, shift, batch, sum(flour), sum(remix), sum(yeast), sum(yield), status, `batch recall` from production group by date_time, product, shift, batch, status, `batch recall` having (date_time between '"+datefrom+"' and '"+dateto+"') and status in "+str(tuple(status))+" and product = '"+product+"';"
    df = pd.read_sql(query, engine)
    return df

def prodreports1p0(dateto,datefrom,status,product):
    query = "select date_time, product, shift, batch, sum(flour), sum(remix), sum(yeast), sum(yield), status, `batch recall` from production group by date_time, product, shift, batch, status, `batch recall` having (date_time between '"+datefrom+"' and '"+dateto+"') and status = '"+status+"' and product in "+str(tuple(product))+";"
    df = pd.read_sql(query, engine)
    return df

def prodreports1p1(dateto,datefrom,status,product):
    query = "select date_time, product, shift, batch, sum(flour), sum(remix), sum(yeast), sum(yield), status, `batch recall` from production group by date_time, product, shift, batch, status, `batch recall` having (date_time between '"+datefrom+"' and '"+dateto+"') and status = '"+status+"' and product = '"+product+"';"
    df = pd.read_sql(query, engine)
    return df

def get_cooling_report(dateto, datefrom, product, pkgcomplete):
    query = "select `date_time`,product,sum(qty),`packaging complete` from cooling group by `date_time`,product,`packaging complete` having (`date_time` between '"+datefrom+"' and '"+dateto+"') and `packaging complete` in "+pkgcomplete+" and product in "+product+";"
    print("hellolo",query)
    df = pd.read_sql(query, engine)
    return df

def get_prod_report(dateto,datefrom,status,product,recall,shift):
    query = "select date_time, product, shift, batch, sum(flour), sum(remix), sum(yeast), sum(yield), status, `batch recall` from production group by date_time, product, shift, batch, status, `batch recall` having (date_time between '"+datefrom+"' and '"+dateto+"') and status in "+status+" and product in "+product+" and `batch recall` in "+recall+" and shift in "+shift+";"
    print("hellolo",query)
    df = pd.read_sql(query, engine)
    return df

def get_store_report(dateto,datefrom,product):
    query = "select date_time,product,sum(`qty received standard`),sum(`qty received rough`), sum(`dispatched standard`), sum(`dispatched rough`), sum(`rough returned bread`), sum(`bread in store`), sum(`rough bread in store`), pkg_supervisor, dsp_supervisor from store group by date_time,product,pkg_supervisor,dsp_supervisor having (date_time between '"+datefrom+"' and '"+dateto+"') and product in "+product+";"
    print("hellolo",query)
    df = pd.read_sql(query, engine)
    return df
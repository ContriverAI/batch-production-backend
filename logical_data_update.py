import threading
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")

def df_bg_cooling(tr,rt):
    query = "update Cooling set `remaining time` = '"+str(rt)+"' where trolley = "+str(tr)+" and `packaging complete` = 'No';"
    with engine.begin() as conn:
        conn.execute(query)

def cooling_update():
    while(True):
        query = "select * from Cooling where `packaging complete` = 'No';"
        df = pd.read_sql(query,engine)
        for i in range(0,len(df)):
            tr = df['trolley'][i]
            t1 = df['complete time'][i]
            t1 = str(t1)
            t1 = t1.split()
            t1 = t1[2]
            print("--time old--------{}----------".format(t1))
            crnttime = time.strftime('%H:%M:%S')
            crnttime = str(crnttime)
            crnttime = crnttime.split()
            crnttime = crnttime[0]
            print("--current time--------{}----------".format(crnttime))
            FMT = '%H:%M:%S'
            tdelta = datetime.strptime(t1, FMT) - datetime.strptime(crnttime, FMT)
            print("--tdelta--------{}----------".format(tdelta))
            print("--tdelta seconds--------{}----------".format(tdelta.seconds))
            if tdelta.seconds == 0 or tdelta.seconds > 5060:
                newtime = "00:00:00"
                print("--newtime--------{}----------".format(newtime))
            else:
                tdelts = timedelta(days=0,seconds=tdelta.seconds, microseconds=tdelta.microseconds)
                newtime = str(tdelts)
                print("--newtime--------{}----------".format(newtime))
            query = "update Cooling set `remaining time` = '"+str(newtime)+"' where trolley = "+str(tr)+";"
            print("--query--{}".format(query))
            x = threading.Thread(target=df_bg_cooling, args=(tr,newtime,))
            x.start()
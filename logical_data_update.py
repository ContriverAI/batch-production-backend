import threading
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")
query = "select * from store;"
data = pd.read_sql(query, engine)

def df_bg_cooling(tr,rt):
    query = "update Cooling set `remaining time` = '"+str(rt)+"' where trolley = "+str(tr)+";"
    with engine.begin() as conn:
        conn.execute(query)

def cooling_update():
    query = "select * from Cooling where `packaging complete` = 'No';"
    df = pd.read_sql(query,engine)
    for i in range(0,len(df)):
        tr = df['trolley'][i]
        t1 = df['complete time'][i]
        t1 = str(t1)
        t1 = t1.split()
        t1 = t1[2]
        crnttime = time.strftime('%H:%M:%S')
        crnttime = str(crnttime)
        crnttime = crnttime.split()
        crnttime = crnttime[0]
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(crnttime, FMT) - datetime.strptime(t1, FMT)
        if tdelta.seconds < 0:
            tdelts = timedelta(days=0,seconds=tdelta.seconds, microseconds=tdelta.microseconds)
            newtime = str(tdelts)
        else:
            newtime = "00:00:00"
        x = threading.Thread(target=df_bg_cooling, args=(tr,newtime,))
        x.start()
    return "cooling updated with complete time"
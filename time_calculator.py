import threading
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

from sqlalchemy import create_engine
#engine = create_engine("mysql+pymysql://testuser:CFB98765@localhost/batch?host=localhost")
engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")

def df_bg_cooling(tr,rt,tod):
    query = "update cooling set `remaining time` = '"+str(rt)+"' where trolley = "+str(tr)+" and `packaging complete` = 'No' and date_time = '"+tod+"';"
    with engine.begin() as conn:
        conn.execute(query)

def calculator():
    query = "select * from cooling where date_time >= subdate(curdate(),1);"
    data = pd.read_sql(query, engine)
    a1 = data['date_time'][0]
    a2 = data['complete time'][0]
    a1 = str(a1).split('-')
    a2 = str(a2).replace('5 days ','')
    a2 = str(a2).split(':')
    a = datetime(int(a1[0]), int(a1[1]), int(a1[2]), int(a2[0]), int(a2[1]), int(a2[2]), 0)
    b = datetime.now()
    c = b - a
    print(str(c.days))
    print(str(c.seconds))
    print(str(c))   
    if c.days == 0:
        if c.seconds > 0:
            newtime = str(c)
        else:
            newtime = "00:00:00"
    elif c.days == -1:
        if c.seconds > 0:
calculator()
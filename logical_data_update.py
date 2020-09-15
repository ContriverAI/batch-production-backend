import threading
import time
import pandas as pd
import numpy as np

from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")
query = "select * from store;"
data = pd.read_sql(query, engine)

for i in range(0,len(data)):
    qrs = data['qty received standard'][i]
    qrr = data['qty received rough'][i]
    ds = data['dispatched standard'][i]
    dr = data['dispatched rough'][i]
    rrb = data['rough returned bread'][i]
    if i == 0:
        bis = qrs + qrr - ds - dr - rrb + data['bread in store'][i]
        rbis = qrr - dr + rrb
    else:
        bis = qrs + qrr - ds - dr - rrb + data['bread in store'][i-1]
        rbis = qrr - dr + rrb
    data['bread in store'][i] = bis
    data['rough bread in store'][i] = rbis
    
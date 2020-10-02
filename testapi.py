from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from datetime import datetime
import sys

query = "select * from production where date_time = curdate();"
engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")

df = pd.read_sql(query, engine)
index_num = list(np.where(((df['batch']=='34')&(df['shift'] == '1')&(df['status']=='Unbaked')))[0])
print(index_num)
print(len(index_num))
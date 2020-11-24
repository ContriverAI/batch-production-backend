from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")

df = pd.read_csv('/home/dev/Desktop/c.csv')
print(df.columns)

def qq(date,flour,shift,remix,yeast,jsp,eco,jex,oyokun,u_key):
    query = "insert into store values('"+str(date)+"','"+str(flour)+"','"+str(shift)+"','"+str(remix)+"','"+str(yeast)+"','"+str(jsp)+"','"+str(eco)+"','"+str(jex)+"','"+str(oyokun)+"','"+str(u_key)+"');"
    with engine.begin() as conn:
        conn.execute(query)
    print(query)
    return 'done'

for i in range(0,len(df)):
    qq(df['DATE'][i],df['PRODUCT'][i],df['QTY RECEIVED STANDARD'][i],df['QTY RECEIVED ROUGH'][i],df['DISPATCHED STANDARD'][i],df['DISPATCHED ROUGH'][i],df['ROUGH RETURNED BREAD'][i],df['BREAD IN STORE'][i],df['ROUGH BREAD IN STORE'][i],'bd6f7e78-f4af-11ea-aed7-00d861da47d1')
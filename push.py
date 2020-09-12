from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")

df = pd.read_csv('/home/dev/Desktop/c.csv')
print(df.columns)

def qq(DATE,TROLLEY,PRODUCT,QTY,TIME,DURATION,COMPLETE,PACKAGING,u_key):
    query = "insert into Cooling values('"+DATE+"','"+str(TROLLEY)+"','"+PRODUCT+"','"+str(QTY)+"','"+TIME+"','"+DURATION+"','"+COMPLETE+"','"+PACKAGING+"','"+u_key+"');"
    with engine.begin() as conn:
        conn.execute(query)
    print(query)
    return 'done'

for i in range(0,len(df)):
    qq(df['DATE'][i],df['TROLLEY'][i],df['PRODUCT'][i],df['QTY'][i],df['TIME IN'][i],df['DURATION'][i],df['COMPLETE TIME'][i],df['PACKAGING COMPLETE'][i],df['u_key'][i])
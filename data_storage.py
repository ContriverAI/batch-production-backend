from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mysql+pymysql://root:Dev@1234@@35.192.39.115/batch?host=35.192.39.115")

def get_users():
    users = pd.read_sql("select * from users;", engine)
    return users

def cooling():
    data = pd.read_sql("select * from Cooling", engine)
    return data


import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()  

#=> Connect to MongodDB 
mogo_uri = os.getenv("MONGO_URI")


#=> Connect to MongodDB server
client = MongoClient(mogo_uri)    

#=> Select database 
db = client["mydatabase"]

def dbconnect():
    return db

   

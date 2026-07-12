from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

# https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/

try: 
    mongo_uri = os.getenv("MONGO_URI") 

    #=> Connect 
    client = MongoClient(mongo_uri) 
    client.admin.command('ping') 
    print("Connected successfully") 

except Exception as e: 
    print("Error: ",e)
finally: 
    #=> Close connection 
    client.close()
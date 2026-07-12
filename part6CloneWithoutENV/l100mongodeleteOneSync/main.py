from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pymongo
from pprint import pprint
from datetime import datetime, timezone
from bson import ObjectId

load_dotenv()

# https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/

try: 
    mongo_uri = os.getenv("MONGO_URI") 

    #=> Connect to MongodDB server
    client = MongoClient(mongo_uri)   

    #=> Select database and collection 
    db = client["mydatabase"]
    collection = db["empolyee"] 


    #=> Input document ID (string) 
    doc_id = input("Enter id: ").strip()
   
    try: 
        object_id = ObjectId(doc_id)
    except Exception: 
        print("Invalid ID Format - must be a valid objectId string.") 
        client.close()
        exit()  

    query_filter = {"_id": object_id}  


    result = collection.delete_one(query_filter) 

    if(result.deleted_count > 0):
        print(f"delete successfully , {result.deleted_count} ")
    


except Exception as e: 
    print("Error: ",e)
finally: 
    #=> Close connection 
    client.close()
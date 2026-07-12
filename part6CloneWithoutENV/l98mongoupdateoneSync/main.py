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

    new_name = input("Enter ner name: ").strip() 
    new_email = input("Enter new email: ").strip()

    query_filter = {"_id": object_id}  

    update_operation = {
        "$set": {
            "username": new_name, 
            "email": new_email
        }
    } 

    result = collection.update_one(query_filter, update_operation) 

    if(result.modified_count > 0):
        print(f"Update successfully , {result.modified_count} = {result.matched_count}")
    
    #=> Get Document by id 
    result = collection.find_one({"_id": object_id})
    if result:
        print(result)
    else: 
        print("No record found with that ID.")


except Exception as e: 
    print("Error: ",e)
finally: 
    #=> Close connection 
    client.close()
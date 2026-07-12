from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime, timezone

load_dotenv()

# https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/

try: 
    mongo_uri = os.getenv("MONGO_URI") 

    #=> Connect to MongodDB server
    client = MongoClient(mongo_uri)   

    #=> Select database and collection 
    db = client["mydatabase"]
    collection = db["empolyee"] 

    data = {
        "username": "aung aung", 
        "email": "aungaung@gmail.com",
        "createdAt": datetime.now(timezone.utc)
    } 

    #=> Inset One document  
    result = collection.insert_one(data)
    #. print(result) #.InsertOneResult(ObjectId('6911f5dc1954c7853270ae9f'), acknowledged=True)
    print(f"Collection {collection.name} is ready in MogoDb! Inserted ID: {result.inserted_id}, {result.acknowledged}")


    client.admin.command('ping') 
    print("Connected successfully") 

except Exception as e: 
    print("Error: ",e)
finally: 
    #=> Close connection 
    client.close()
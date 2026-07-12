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

    datas = [
       ("zaw zaw","zawzaw@gmail.com"), 
       ("naw naw", "nawnaw@gmail.com")
    ] 

    documents = [] 

    for username, emial in datas: 
        documents.append({
            "username": username, 
            "email": emial, 
            "createdAt": datetime.now(timezone.utc)
        }) 
    

    #=> Inset Multi document  
    result = collection.insert_many(documents)

    print(f"Collection {collection.name} is ready in MogoDb! Inserted ID: {result.inserted_ids}, {result.acknowledged}")
    print(f"{len(result.inserted_ids)} documents inserted.")  # 2 documents inserted.




except Exception as e: 
    print("Error: ",e)
finally: 
    #=> Close connection 
    client.close()
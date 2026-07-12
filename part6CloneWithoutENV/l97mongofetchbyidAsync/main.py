from dotenv import load_dotenv
import os
from pymongo import AsyncMongoClient
import pymongo
from pprint import pprint
from datetime import datetime, timezone
import asyncio
from bson import ObjectId

load_dotenv()

# https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/

async def main():
    try: 
        mongo_uri = os.getenv("MONGO_URI") 

        #=> Connect to MongodDB server
        client = AsyncMongoClient(mongo_uri)   

        #=> Select database and collection 
        db = client["mydatabase"]
        collection = db["empolyee"] 

         #=> Input document ID (string) 
        doc_id = input("Enter id: ").strip()
        try: 
            object_id = ObjectId(doc_id)
        except Exception: 
            print("Invalid ID Format - must be a valid objectId string.") 
            await client.close()
            exit() 

        
        #=> Get Document by id 
        result = await collection.find_one({"_id": object_id})
        if result:
            print(result)
        else: 
            print("No record found with that ID.")



    except Exception as e: 
        print("Error: ",e)
    finally: 
        #=> Close connection 
        await client.close() 

if __name__ == "__main__":
    asyncio.run(main())


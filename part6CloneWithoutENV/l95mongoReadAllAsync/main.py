from dotenv import load_dotenv
import os
from pymongo import AsyncMongoClient
import pymongo
from pprint import pprint
from datetime import datetime, timezone
import asyncio

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

        count = await collection.count_documents({})
        print(f"Total documents count: {count}") 

        #=> Fetch all 
        print("\n fetch all documents \n") 
        # results = collection.find().sort("createdAt", pymongo.DESCENDING)
        results = collection.find({}).sort("createdAt", pymongo.DESCENDING)
        # results = collection.find({}).sort("createdAt", pymongo.ASCENDING)

        async for result in results:
            pprint({
                "ID": str(result.get("_id")),
                "Name": result.get("username"),
                "Email": result.get("email"),
                "Created": result.get("createdAt"),
            }) 


        #=> Fetch some 
        # print("\n fetch some documents \n") 
        # results = collection.find({}).sort("createdAt", pymongo.DESCENDING).limit(2)
        # # results = collection.find({}).sort("createdAt", pymongo.ASCENDING).limit(2)

        # async for result in results:
        #     pprint({
        #         "ID": str(result.get("_id")),
        #         "Name": result.get("username"),
        #         "Email": result.get("email"),
        #         "Created": result.get("createdAt"),
        #     }) 


        #=> Fetch One 
        # print("\n Fetch First documents \n") 
        # results = collection.find({}).sort("createdAt", pymongo.ASCENDING).limit(1) 

        # first_doc = await results.to_list()
        # # print(first_doc)  # [{'_id': ObjectId('6911f5829c38ece87d611cb9'), 'username': 'aung aung', 'email': 'aungaung@gmail.com', 'createdAt': datetime.datetime(2025, 11, 10, 14, 24, 2, 276000)}] 

        # if first_doc:
        #     pprint({
        #         "ID": str(first_doc[0].get("_id")),
        #         "Name": first_doc[0].get("username"),
        #         "Email": first_doc[0].get("email"),
        #         "Created": first_doc[0].get("createdAt"),
        #     }) 
        # else: 
        #     print("No documents found.")

        



    except Exception as e: 
        print("Error: ",e)
    finally: 
        #=> Close connection 
        await client.close() 

if __name__ == "__main__":
    asyncio.run(main())


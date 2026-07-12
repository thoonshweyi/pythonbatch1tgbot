from dotenv import load_dotenv
import os
import asyncio
import pymongo
from pymongo import AsyncMongoClient
from datetime import datetime, timezone

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

        datas = [
            {
                "username": "nu nu", 
                "email": "nunu@gmail.com",
                "createdAt": datetime.now(timezone.utc)
            }, 
            {
                "username": "ae ae", 
                "email": "aeae@gmail.com",
                "createdAt": datetime.now(timezone.utc)
            } 
        ]

        #=> Inset One document  
        result = await collection.insert_many(datas)
        print(f"Collection {collection.name} is ready in MogoDb! Inserted ID: {result.inserted_id}, {result.acknowledged}")


    except Exception as e: 
        print("Error: ",e)
    finally: 
        #=> Close connection 
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())



# | Situation                                        | Should you `ping()`? | Why                                                 |
# | ------------------------------------------------ | -------------------- | --------------------------------------------------- |
# | Just inserting/reading right away                | ❌ Not needed         | Operations already test connection                  |
# | Doing a connection test before operations        | ✅ Yes                | Forces early connection check                       |
# | Running a web service that needs DB health check | ✅ Yes                | Verifies DB availability on startup or periodically |

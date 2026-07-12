from dotenv import load_dotenv
import os
from pymongo import AsyncMongoClient
import asyncio

load_dotenv()

# https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/


async def main():
    try: 
        mongo_uri = os.getenv("MONGO_URI") 

        #=> Connect 
        client = AsyncMongoClient(mongo_uri) 
        await client.admin.command("ping")
        print("Connected successfully") 

    except Exception as e: 
        print("Error: ",e)
    finally: 
        #=> Close connection 
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())

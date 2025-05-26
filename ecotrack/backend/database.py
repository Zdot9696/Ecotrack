from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://danvargas1996:Cluster1996@cluster0.5kzqtyj.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URL)

db = client.ecotrack_db  # La base de datos

import motor.motor_asyncio
# Conecta no BD
conn_str = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
db = client.provenance
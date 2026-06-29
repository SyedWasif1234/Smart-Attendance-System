from prisma import Prisma

db = Prisma()

async def connect_db():
    await db.connect()
    print("Databse connected successfully")

async def disconnect_db():
    await db.disconnect()
    print("Databse disconnected successfully")


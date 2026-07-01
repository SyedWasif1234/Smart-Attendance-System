from prisma import Prisma

db = Prisma()

async def connect_db():
    await db.connect()
    print("Database connected successfully")

async def disconnect_db():
    await db.disconnect()
    print("Database disconnected successfully")

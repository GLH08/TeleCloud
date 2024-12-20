import asyncio
from src.database.database import Database
from config.settings import Settings

async def init_database():
    """Initialize database tables"""
    settings = Settings()
    db = Database(settings.DATABASE_URL)
    
    try:
        await db.init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    asyncio.run(init_db())

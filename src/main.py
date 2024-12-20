import asyncio
import logging
from telegram.ext import Application, MessageHandler, CommandHandler, filters

from config.settings import Settings
from src.bot.handlers.command_handler import CommandHandlers
from src.bot.handlers.file_handler import FileHandler
from src.storage.onedrive import OneDriveStorage
from src.database.database import Database

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    # Load settings
    settings = Settings()
    
    # Initialize components
    db = Database(settings.DATABASE_URL)
    storage = OneDriveStorage(
        client_id=settings.ONEDRIVE_CLIENT_ID,
        client_secret=settings.ONEDRIVE_CLIENT_SECRET
    )
    
    # Initialize bot application
    application = Application.builder().token(settings.BOT_TOKEN).build()
    
    # Initialize handlers
    command_handlers = CommandHandlers(db, storage)
    file_handler = FileHandler(db, storage)
    
    # Add handlers
    application.add_handler(CommandHandler("start", command_handlers.start))
    application.add_handler(CommandHandler("help", command_handlers.help))
    application.add_handler(CommandHandler("stats", command_handlers.stats))
    application.add_handler(MessageHandler(filters.Document.ALL, file_handler.handle_file))
    
    # Start bot
    await application.initialize()
    await application.start()
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

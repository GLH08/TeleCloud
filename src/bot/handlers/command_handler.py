from telegram import Update
from telegram.ext import ContextTypes

class CommandHandlers:
    def __init__(self, db, storage):
        self.db = db
        self.storage = storage

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        user = update.effective_user
        welcome_message = (
            f"👋 Welcome {user.first_name}!\n\n"
            "I can help you store files in the cloud. Simply send me any file "
            "and I'll upload it to your cloud storage.\n\n"
            "Available commands:\n"
            "/help - Show this help message\n"
            "/stats - Show your storage statistics"
        )
        await update.message.reply_text(welcome_message)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        help_text = (
            "🔍 Available Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/stats - Show your storage statistics\n\n"
            "📤 To upload a file:\n"
            "Simply send me any file and I'll upload it to the cloud."
        )
        await update.message.reply_text(help_text)

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /stats command"""
        user_id = update.effective_user.id
        stats = await self.db.get_user_stats(user_id)
        
        stats_text = (
            "📊 Your Storage Statistics:\n\n"
            f"Files uploaded: {stats['total_files']}\n"
            f"Total size: {stats['total_size_formatted']}\n"
            f"Available space: {stats['available_space_formatted']}"
        )
        await update.message.reply_text(stats_text)

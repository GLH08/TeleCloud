import os
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.file_utils import get_file_size_formatted, is_valid_file

class FileHandler:
    def __init__(self, db, storage):
        self.db = db
        self.storage = storage

    async def handle_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle file uploads"""
        user_id = update.effective_user.id
        
        # Check if user is authorized
        if not await self.db.is_user_authorized(user_id):
            await update.message.reply_text(
                "⚠️ You are not authorized to use this bot."
            )
            return

        # Get file information
        file = update.message.document
        if not file:
            await update.message.reply_text("⚠️ Please send a valid file.")
            return

        # Validate file
        if not is_valid_file(file):
            await update.message.reply_text(
                "⚠️ File type not supported or file too large."
            )
            return

        try:
            # Send processing message
            status_message = await update.message.reply_text(
                "📤 Processing your file..."
            )

            # Download file
            file_path = f"/app/data/uploads/{file.file_name}"
            await context.bot.get_file(file.file_id).download_to_drive(file_path)

            # Upload to cloud storage
            share_link = await self.storage.upload_file(file_path, file.file_name)

            # Update database
            await self.db.add_file_record(
                user_id=user_id,
                file_name=file.file_name,
                file_size=file.file_size,
                share_link=share_link
            )

            # Send success message
            await status_message.edit_text(
                f"✅ File uploaded successfully!\n\n"
                f"📎 Share link: {share_link}"
            )

        except Exception as e:
            await status_message.edit_text(
                f"❌ Upload failed: {str(e)}"
            )
        finally:
            # Cleanup temporary file
            if os.path.exists(file_path):
                os.remove(file_path)

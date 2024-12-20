from typing import Union
from telegram import Document
from config.settings import Settings

settings = Settings()

def get_file_size_formatted(size_in_bytes: int) -> str:
    """Convert file size to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

def is_valid_file(file: Document) -> bool:
    """
    Validate file based on size and type
    """
    # Check file size
    if file.file_size > settings.MAX_FILE_SIZE:
        return False
    
    # Check file type if specific types are set
    if settings.ALLOWED_MIME_TYPES != ["*/*"]:
        if file.mime_type not in settings.ALLOWED_MIME_TYPES:
            return False
    
    return True

def get_file_extension(file_name: str) -> str:
    """Get file extension from filename"""
    return file_name.split('.')[-1] if '.' in file_name else ''

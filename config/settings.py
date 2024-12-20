from pydantic import BaseSettings, validator
from typing import List, Set
import json

class Settings(BaseSettings):
    # Bot Configuration
    BOT_TOKEN: str
    ADMIN_USER_IDS: Set[int] = set()
    
    # OneDrive Configuration
    ONEDRIVE_CLIENT_ID: str
    ONEDRIVE_CLIENT_SECRET: str
    ONEDRIVE_REDIRECT_URI: str
    
    # Database Configuration
    DATABASE_URL: str
    
    # Redis Configuration
    REDIS_URL: str
    
    # Storage Configuration
    MAX_FILE_SIZE: int = 2147483648  # 2GB in bytes
    ALLOWED_MIME_TYPES: List[str] = ["*/*"]
    UPLOAD_FOLDER: str = "/app/data/uploads"
    
    # Rate Limiting
    RATE_LIMIT_CALLS: int = 30
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # User Quotas (in bytes)
    DEFAULT_USER_QUOTA: int = 5368709120  # 5GB
    PREMIUM_USER_QUOTA: int = 53687091200  # 50GB
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "/app/logs/telecloud.log"
    
    @validator('ADMIN_USER_IDS', pre=True)
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return set(int(x.strip()) for x in v.split(','))
        return v
    
    @validator('ALLOWED_MIME_TYPES', pre=True)
    def parse_mime_types(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    class Config:
        env_file = '.env'
        case_sensitive = True

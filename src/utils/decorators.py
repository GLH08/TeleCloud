import functools
from telegram import Update
from config.settings import Settings

settings = Settings()

def admin_only(func):
    """Decorator to restrict command to admin users only"""
    @functools.wraps(func)
    async def wrapper(self, update: Update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in settings.ADMIN_USER_IDS:
            await update.message.reply_text("⚠️ This command is restricted to administrators only.")
            return
        return await func(self, update, context, *args, **kwargs)
    return wrapper

def rate_limit(calls: int, period: int):
    """
    Rate limiting decorator
    :param calls: Number of calls allowed
    :param period: Time period in seconds
    """
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        async def wrapper(self, update: Update, context, *args, **kwargs):
            user_id = update.effective_user.id
            current_time = time.time()
            
            if user_id in cache:
                calls_made, first_call = cache[user_id]
                
                if current_time - first_call > period:
                    cache[user_id] = (1, current_time)
                elif calls_made >= calls:
                    wait_time = int(period - (current_time - first_call))
                    await update.message.reply_text(
                        f"⚠️ Rate limit exceeded. Please wait {wait_time} seconds."
                    )
                    return
                else:
                    cache[user_id] = (calls_made + 1, first_call)
            else:
                cache[user_id] = (1, current_time)
            
            return await func(self, update, context, *args, **kwargs)
        return wrapper
    return decorator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    storage_quota = Column(Integer, default=5368709120)  # 5GB in bytes

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_name = Column(String)
    file_size = Column(Integer)
    share_link = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_user(self, telegram_id: int):
        async with self.SessionLocal() as session:
            result = await session.query(User).filter(
                User.telegram_id == telegram_id
            ).first()
            return result

    async def add_file_record(self, user_id: int, file_name: str, 
                            file_size: int, share_link: str):
        async with self.SessionLocal() as session:
            file_record = File(
                user_id=user_id,
                file_name=file_name,
                file_size=file_size,
                share_link=share_link
            )
            session.add(file_record)
            await session.commit()
            return file_record

    async def get_user_stats(self, telegram_id: int):
        async with self.SessionLocal() as session:
            user = await self.get_user(telegram_id)
            if not user:
                return None
                
            files = await session.query(File).filter(
                File.user_id == user.id
            ).all()
            
            total_size = sum(f.file_size for f in files)
            available_space = user.storage_quota - total_size
            
            return {
                'total_files': len(files),
                'total_size': total_size,
                'total_size_formatted': self._format_size(total_size),
                'available_space': available_space,
                'available_space_formatted': self._format_size(available_space)
            }

    def _format_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

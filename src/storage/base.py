from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    async def upload_file(self, file_path: str, destination: str) -> str:
        """Upload a file to storage and return share link"""
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage"""
        pass

    @abstractmethod
    async def get_file_info(self, file_path: str) -> dict:
        """Get file information"""
        pass

    @abstractmethod
    async def create_share_link(self, file_path: str) -> str:
        """Create a sharing link for the file"""
        pass

import aiohttp
from msal import ConfidentialClientApplication
from src.storage.base import BaseStorage
from config.settings import Settings

class OneDriveStorage(BaseStorage):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.settings = Settings()
        self.app = ConfidentialClientApplication(
            client_id=client_id,
            client_secret=client_secret,
            authority="https://login.microsoftonline.com/common"
        )

    async def get_access_token(self):
        """Get OneDrive access token"""
        result = await self.app.acquire_token_silent(
            ["Files.ReadWrite.All"],
            account=None
        )
        
        if not result:
            result = await self.app.acquire_token_for_client(
                ["https://graph.microsoft.com/.default"]
            )
        
        return result['access_token']

    async def upload_file(self, file_path: str, destination: str) -> str:
        """Upload file to OneDrive"""
        token = await self.get_access_token()
        
        # For files smaller than 4MB, use simple upload
        if os.path.getsize(file_path) < 4 * 1024 * 1024:
            return await self._simple_upload(file_path, destination, token)
        else:
            return await self._large_file_upload(file_path, destination, token)

    async def _simple_upload(self, file_path: str, destination: str, token: str) -> str:
        """Simple upload for small files"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream"
        }
        
        async with aiohttp.ClientSession() as session:
            with open(file_path, 'rb') as f:
                async with session.put(
                    f"https://graph.microsoft.com/v1.0/me/drive/root:/{destination}:/content",
                    headers=headers,
                    data=f
                ) as response:
                    if response.status == 201 or response.status == 200:
                        data = await response.json()
                        return data['webUrl']
                    else:
                        raise Exception(f"Upload failed: {await response.text()}")

    async def _large_file_upload(self, file_path: str, destination: str, token: str) -> str:
        """Upload large files using upload session"""
        # Implementation for large file upload
        # This would involve creating an upload session and uploading the file in chunks
        pass

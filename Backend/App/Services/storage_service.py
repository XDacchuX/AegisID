import httpx
import json
from fastapi import HTTPException
from app.core.config import settings
from app.core.security import encrypt_data, decrypt_data

W3UP_UPLOAD_URL = "https://up.web3.storage/upload"
W3UP_GATEWAY = "https://w3s.link/ipfs/"

class StorageService:
    @staticmethod
    async def upload_to_w3up(user_id: str, descriptor: list) -> str:
        """Encrypt and upload to w3up. Returns ipfs:// CID"""
        try:
            payload = json.dumps({"user_id": user_id, "descriptor": descriptor}).encode()
            encrypted = encrypt_data(payload)

            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {'file': (f'{user_id}.bin', encrypted, 'application/octet-stream')}
                headers = {'Authorization': f'Bearer {settings.W3UP_TOKEN}'}
                res = await client.post(W3UP_UPLOAD_URL, files=files, headers=headers)
                res.raise_for_status()

            cid = res.json()["cid"]
            return f"ipfs://{cid}"
        except Exception as e:
            raise HTTPException(500, f"w3up upload failed: {str(e)}")

    @staticmethod
    async def download_from_w3up(cid: str) -> list:
        """Download and decrypt descriptor from IPFS"""
        try:
            url = f"{W3UP_GATEWAY}{cid.replace('ipfs://', '')}"
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.get(url)
                res.raise_for_status()

            decrypted = decrypt_data(res.content)
            data = json.loads(decrypted)
            return data["descriptor"]
        except Exception as e:
            raise HTTPException(500, f"w3up download failed: {str(e)}")

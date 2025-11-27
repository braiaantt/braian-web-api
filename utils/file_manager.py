import uuid
import os
from fastapi import UploadFile
from exceptions import InvalidContentType


class FileManager:
    STATIC_ROOT = "static"               
    TECHNOLOGY_FOLDER = "technologies"

    @staticmethod
    async def save_technology_image(file: UploadFile) -> str:

        if not file.content_type.startswith("image/"):
            raise InvalidContentType()

        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"

        folder_path = os.path.join(FileManager.STATIC_ROOT, FileManager.TECHNOLOGY_FOLDER)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, unique_name)

        file_bytes = await file.read()
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        public_path = f"/static/{FileManager.TECHNOLOGY_FOLDER}/{unique_name}"

        return public_path

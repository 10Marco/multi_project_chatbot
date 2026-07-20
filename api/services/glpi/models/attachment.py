import os
from dataclasses import dataclass
from fastapi import UploadFile
from services.glpi.models.base_model import BaseModel


@dataclass
class Attachment(BaseModel):

    filename: str
    mimetype: str
    size: int
    local_path: str

    @classmethod
    def from_upload(
        cls,
        file: UploadFile,
        local_path: str
    ):

        return cls(
            filename=file.filename,
            mimetype=file.content_type,
            size=os.path.getsize(local_path),
            local_path=local_path
        )

    def exists(self):
        return os.path.exists(self.local_path)
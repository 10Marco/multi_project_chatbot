from services.glpi.models.attachment import Attachment

import os
import shutil
import tempfile


class PayloadFactory:

    @staticmethod
    async def create(
        sender,
        message,
        file
    ):

        payload = {
            "sender": sender,
            "message": message
        }

        if not file:
            return payload

        temp_dir = tempfile.mkdtemp()

        file_path = os.path.join(
            temp_dir,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        payload["attachment"] = Attachment.from_upload(
            file,
            file_path
        )

        return payload
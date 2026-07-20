import os

from services.glpi.client import upload_document_glpi


class AttachmentService:

    def process(self, ticket_id, attachments):

        for attachment in attachments:

            if not attachment.exists():
                raise FileNotFoundError(attachment.local_path)

            self.upload(ticket_id, attachment)

            self.cleanup(attachment)

    def upload(self, ticket_id, attachment):
        return upload_document_glpi(
            ticket_id,
            attachment
        )

    def cleanup(self, attachment):
        try:
            if os.path.exists(attachment.local_path):
                os.remove(attachment.local_path)
        except Exception as e:
            print(f"Erro ao remover {attachment.local_path}: {e}")
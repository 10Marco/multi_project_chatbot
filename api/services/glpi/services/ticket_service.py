from services.glpi.builders.ticket_builder import build_ticket
from services.glpi.client import create_ticket_glpi
from services.glpi.services.attachment_service import AttachmentService
from utils.logger import debug


class TicketService:

    def __init__(self):
        self.attachments = AttachmentService()

    def create(self, ticket):
        payload = build_ticket(ticket)
        ticket_id = create_ticket_glpi(payload)
        if ticket.attachments:
            for attachment in ticket.attachments:
                debug(
                    "Attachment: nome=%s tipo=%s tamanho=%s caminho=%s",
                    attachment.filename,
                    attachment.mimetype,
                    attachment.size,
                    attachment.local_path,
                )

            self.attachments.process(
                ticket_id,
                ticket.attachments
            )
        return ticket_id

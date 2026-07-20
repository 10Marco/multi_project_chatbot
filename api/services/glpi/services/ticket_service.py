from services.glpi.builders.ticket_builder import build_ticket
from services.glpi.client import create_ticket_glpi
from services.glpi.services.attachment_service import AttachmentService


class TicketService:

    def __init__(self):
        self.attachments = AttachmentService()

    def create(self, ticket):
        payload = build_ticket(ticket)
        ticket_id = create_ticket_glpi(payload)
        if ticket.attachments:
            print("\n===== ATTACHMENTS =====")

            for attachment in ticket.attachments:
                print(f"Nome: {attachment.filename}")
                print(f"Tipo: {attachment.mimetype}")
                print(f"Tamanho: {attachment.size}")
                print(f"Caminho: {attachment.local_path}")
                print("-----------------------")

            self.attachments.process(
                ticket_id,
                ticket.attachments
            )
        return ticket_id
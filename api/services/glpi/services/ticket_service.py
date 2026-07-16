from services.glpi.builders.ticket_builder import build_ticket
from services.glpi.client import criar_ticket_glpi


def create_ticket(ticket):

    payload = build_ticket(ticket)

    return criar_ticket_glpi(payload)
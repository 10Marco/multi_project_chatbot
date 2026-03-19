from glpi import get_session, create_ticket

def criar_ticket_glpi(sender, message):
    session = get_session()
    return create_ticket(session, sender, message)
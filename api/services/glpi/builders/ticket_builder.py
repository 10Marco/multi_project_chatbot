from services.glpi.models.ticket import Ticket


def build_ticket(ticket: Ticket):
    payload = {
        "name": ticket.title,
        "content": ticket.description,
        "type": ticket.type,
    }

    optional_fields = {
        "itilcategories_id": ticket.category,
        "locations_id": ticket.location,
        "_users_id_requester": ticket.requester_id(),
    }

    payload.update(
        {key: value for key, value in optional_fields.items() if value is not None}
    )

    return {"input": payload}
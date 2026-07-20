from services.glpi.models.requester import Requester
from services.glpi.models.ticket import Ticket
from services.glpi.models.conversation import Conversation
from services.glpi.models.attachment import Attachment


def conversation_from_dict(data):

    ticket_data = data.get("ticket", {})

    requester = None

    if ticket_data.get("requester"):
        requester = Requester(
            **ticket_data["requester"]
        )

    attachments = []

    for item in ticket_data.get("attachments", []):
        if isinstance(item, Attachment):
            attachments.append(item)
        else:
            attachments.append(Attachment(**item))

    ticket = Ticket(
        requester=requester,
        title=ticket_data.get("title"),
        description=ticket_data.get("description"),
        category=ticket_data.get("category"),
        location=ticket_data.get("location"),
        type=ticket_data.get("type", 2),
        attachments=attachments,
        metadata=ticket_data.get("metadata", {})
    )

    return Conversation(
        step=data.get("step", ""),
        ticket=ticket,
        context=data.get("context", {}),
        updated_at=data.get("updated_at", 0)
    )
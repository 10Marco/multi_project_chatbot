from services.glpi.models.ticket import Ticket
from services.glpi.models.conversation import Conversation


def conversation_from_dict(data: dict) -> Conversation:

    ticket = Ticket(**data.get("ticket", {}))

    return Conversation(

        step=data.get("step", ""),

        ticket=ticket,

        context=data.get("context", {})

    )
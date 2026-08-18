from services.glpi.conversation_service import ConversationService

conversation = ConversationService()

def to_whatsapp(reply):

    builders = {

        "text": lambda r: {
            "type": "text",
            "text": r.data["text"]
        },

        "image": lambda r: {
            "type": "image",
            **r.data
        },

        "document": lambda r: {
            "type": "document",
            **r.data
        },

        "buttons": lambda r: {
            "type": "buttons",
            **r.data
        },

        "list": lambda r: {
            "type": "list",
            **r.data
        },
        "sifop_folha": lambda r: {
            "type": "sifop_folha",
            **r.data
        },
        

    }

    if reply.type not in builders:

        raise ValueError(f"Tipo desconhecido: {reply.type}")

    return builders[reply.type](reply)


def handle_glpi_flow(sender, message, payload=None):

    reply = conversation.handle(
        sender,
        message,
        payload
    )

    return [
        to_whatsapp(reply)
    ]
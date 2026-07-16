from services.glpi.conversation_service import ConversationService

conversation = ConversationService()


def to_whatsapp(reply):

    if reply.type == "text":

        return {

            "type": "text",

            "text": reply.data["text"]

        }

    if reply.type == "image":

        return {

            "type": "image",

            **reply.data

        }

    if reply.type == "document":

        return {

            "type": "document",

            **reply.data

        }

    if reply.type == "buttons":

        return {

            "type": "buttons",

            **reply.data

        }

    if reply.type == "list":

        return {

            "type": "list",

            **reply.data

        }

    raise ValueError(f"Tipo desconhecido: {reply.type}")


def handle_glpi_flow(sender, message, payload=None):

    reply = conversation.handle(
        sender,
        message,
        payload
    )

    return [

        to_whatsapp(reply)

    ]
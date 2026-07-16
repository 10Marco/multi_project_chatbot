from services.glpi.flow import handle_glpi_flow


def route_conversation(project, sender, message, payload):

    messages = handle_glpi_flow(
        sender,
        message,
        payload
    )

    return {

        "source": "glpi",

        "messages": messages

    }
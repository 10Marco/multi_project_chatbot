from services.glpi.flow import handle_glpi_flow

ROUTERS = {
    "GLPI": handle_glpi_flow,
}


def route_conversation(project, sender, message, payload):

    handler = ROUTERS.get(project)

    if not handler:
        raise ValueError(f"Projeto desconhecido: {project}")

    messages = handler(
        sender,
        message,
        payload
    )

    return {
        "source": project.lower(),
        "messages": messages
    }
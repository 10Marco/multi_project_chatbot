import os

PROJECT = os.getenv("PROJECT", "glpi")


def handle_action(action, payload):
    sender = payload.get("sender")
    message = payload.get("message")

    # 🔵 GLPI
    if action == "create_ticket" and PROJECT == "glpi":
        from glpi import get_session, create_ticket

        session = get_session()
        ticket_id = create_ticket(session, sender, message)

        return [
            f"✅ Chamado criado com sucesso!\n\nNúmero: {ticket_id}"
        ]

    # 🟡 GARAGEM
    if action == "create_ticket" and PROJECT == "garagem":
        return [
            "🔧 Pedido recebido!",
            "Nossa equipe vai te responder com o orçamento em breve."
        ]

    # 🟢 LOJA
    if action == "create_ticket" and PROJECT == "loja":
        return [
            "🛒 Pedido registrado!",
            "Entraremos em contato para finalizar a compra."
        ]

    return ["⚠️ Ação não implementada."]
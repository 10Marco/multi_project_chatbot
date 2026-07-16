from core.project_resolver import get_projeto
from core.conversation_router import route_conversation
from services.glpi.models.reply import Reply


class ChatOrchestrator:

    def handle(self, payload: dict):

        sender = payload.get("from") or payload.get("sender")

        raw_message = payload.get("message") or payload.get("body") or ""
        message = raw_message.strip().lower()

        projeto = get_projeto(sender)

        print(f"\n📥 [{projeto}] USER: {sender}")
        print(f"➡️ RAW: {raw_message}")
        print(f"➡️ NORMALIZED: {message}")

        try:
            routed = route_conversation(projeto, sender, raw_message, payload)

            return {
                "to": sender,
                "project": projeto,
                "source": routed["source"],
                "messages": routed["messages"],
            }

        except Exception as e:

            print(f"[ORCHESTRATOR ERROR] {e}")

            return {
                "to": sender,
                "project": projeto,
                "messages": [
                    Reply.text("❌ Erro interno.")
                ]
            }
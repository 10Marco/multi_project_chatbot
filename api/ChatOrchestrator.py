from core.project_resolver import get_project
from core.conversation_router import route_conversation
from utils.debug import debug_reply


class ChatOrchestrator:

    def handle(self, payload: dict):
        sender = payload.get("from") or payload.get("sender")
        raw_message = payload.get("message") or payload.get("body") or ""
        project = get_project(sender)

        print(f"\n📥 [{project}] USER: {sender}")
        print(f"➡️ RAW: {raw_message}")

        try:
            routed = route_conversation(
                project,
                sender,
                raw_message,
                payload
            )

            return {
                "to": sender,
                "project": project,
                "source": routed["source"],
                "messages": routed["messages"],
            }

        except Exception as e:
            return {
                "to": sender,
                "project": project,
                "messages": [
                    debug_reply(e)
                ]
            }
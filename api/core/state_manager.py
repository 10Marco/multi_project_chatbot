import json
import time

from dataclasses import asdict

from redis_client import r

from services.glpi.models.conversation import Conversation
from services.glpi.models.converters import conversation_from_dict


class StateManager:

    TTL = 600

    def _key(self, sender):
        return f"user:{sender}:session"

    def get(self, sender):

        data = r.get(self._key(sender))

        if not data:
            return Conversation()

        return conversation_from_dict(
            json.loads(data)
        )

    def save(self, sender, conversation: Conversation):

        conversation.updated_at = int(time.time())

        r.set(

            self._key(sender),

            json.dumps(asdict(conversation)),

            ex=self.TTL

        )

    def clear(self, sender):

        r.delete(self._key(sender))
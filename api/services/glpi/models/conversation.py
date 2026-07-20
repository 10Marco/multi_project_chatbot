from dataclasses import dataclass, field
import time
from services.glpi.models.ticket import Ticket
from services.glpi.models.base_model import BaseModel

@dataclass
class Conversation(BaseModel):

    step: str = ""
    ticket: Ticket = field(default_factory=Ticket)
    context: dict = field(default_factory=dict)
    updated_at: int = field(default_factory=lambda: int(time.time()))

    def reset(self):
        self.step = ""
        self.ticket = Ticket()
        self.context.clear()
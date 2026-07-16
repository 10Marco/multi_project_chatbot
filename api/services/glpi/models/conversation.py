from dataclasses import dataclass, field
import time

from services.glpi.models.ticket import Ticket

@dataclass
class Conversation:

    step: str = ""

    ticket: Ticket = field(default_factory=Ticket)

    context: dict = field(default_factory=dict)

    updated_at: int = field(default_factory=lambda: int(time.time()))
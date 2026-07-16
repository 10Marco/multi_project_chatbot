from dataclasses import dataclass, field, asdict
from typing import Optional

from services.glpi.models.requester import Requester


@dataclass
class Ticket:

    requester: Optional[Requester] = None

    title: Optional[str] = None

    description: Optional[str] = None

    category: Optional[int] = None

    location: Optional[int] = None

    type: int = 2

    attachments: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def requester_id(self):

        return self.requester.id if self.requester else None

    def requester_name(self):

        return self.requester.name if self.requester else None

    def to_dict(self):

        return asdict(self)
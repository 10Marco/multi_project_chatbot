from dataclasses import dataclass, field
from typing import Optional
from services.glpi.models.base_model import BaseModel
from services.glpi.models.attachment import Attachment
from services.glpi.models.requester import Requester

@dataclass
class Ticket(BaseModel):

    requester: Optional[Requester] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[int] = None
    location: Optional[int] = None
    type: int = 2
    attachments: list[Attachment] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def requester_id(self):
        return self.requester.id if self.requester else None

    @property
    def requester_name(self):
        return self.requester.name if self.requester else None
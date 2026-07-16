from dataclasses import dataclass
from typing import Optional


@dataclass
class Requester:

    id: int

    name: str

    firstname: str | None = None

    realname: str | None = None

    registration: str | None = None

    phone: str | None = None

    mobile: str | None = None

    email: str | None = None

    entity_id: int | None = None

    group_id: int | None = None

    location_id: int | None = None

    entity: dict | None = None

    group: dict | None = None

    location: dict | None = None

    is_active: bool = True
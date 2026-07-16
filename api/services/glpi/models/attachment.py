from dataclasses import dataclass

@dataclass
class Attachment:

    filename: str

    mime: str

    path: str

    size: int
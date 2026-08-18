from dataclasses import dataclass

@dataclass
class TicketSummary:
    id: int
    name: str

    def url(self, base_url: str) -> str:
        return f"{base_url}/front/ticket.form.php?id={self.id}"
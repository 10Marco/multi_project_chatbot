from .repositories.user_repository import UserRepository
from .repositories.chatbot_repository import ChatbotRepository
from .repositories.ticket_repository import TicketRepository
from .repositories.location_repository import LocationRepository
from .repositories.category_repository import CategoryRepository
from .repositories.group_repository import GroupRepository
from .repositories.entity_repository import EntityRepository
from .services.ticket_service import TicketService

from utils.logger import debug

import os


class GLPIService:

    def __init__(self):

        self.web_url = os.getenv("GLPI_WEB_URL")

        self.users = UserRepository()
        self.chatbot = ChatbotRepository()

        self.tickets = TicketRepository()
        self.ticket_service = TicketService()

        self.locations = LocationRepository()
        self.categories = CategoryRepository()
        self.groups = GroupRepository()
        self.entities = EntityRepository()

    def identify_user(self, phone):

        debug(
            "[IDENTIFY] procurando mobile: %s",
            phone
        )

        user = self.users.find_by_mobile(phone)

        if not user:

            debug(
                "[IDENTIFY] mobile não autorizado: %s",
                phone
            )

            return None

        debug(
            "[IDENTIFY] usuário identificado: %s (%s)",
            user.name,
            user.id
        )

        debug(
            "[IDENTIFY] SIFOP: id=%s tipo=%s",
            user.id_sifop,
            user.tipo
        )

        return user

    def search_user(self, text):

        return self.users.search(text)

    def link_phone(self, requester, phone):

        self.chatbot.link_phone(
            requester.id,
            phone
        )

    def get_open_tickets(self, requester):

        return self.tickets.find_open_by_requester(
            requester.id
        )

    def create_ticket(self, ticket):

        return self.ticket_service.create(ticket)


    def get_location(self, requester):

        if requester.location_id:

            return self.locations.find_by_id(
                requester.location_id
            )

    def get_group(self, requester):

        if requester.group_id:

            return self.groups.find_by_id(
                requester.group_id
            )

    def get_entity(self, requester):

        if requester.entity_id:

            return self.entities.find_by_id(
                requester.entity_id
            )

    def get_default_category(self):

        return self.categories.find_by_id(47)

    def get_ticket_url(self, ticket_id):

        return (
            f"{self.web_url}/front/ticket.form.php"
            f"?id={ticket_id}"
        )
    
    def get_sifop_data(self, requester):

        mapping = self.chatbot.find_by_user_id(requester.id)

        if not mapping:
            return None

        return {
            "id_sifop": mapping["id_sifop"],
            "tipo": mapping["tipo"]
        }
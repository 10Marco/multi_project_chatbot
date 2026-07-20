from .repositories.user_repository import UserRepository
from .repositories.chatbot_repository import ChatbotRepository
from .repositories.ticket_repository import TicketRepository
from .repositories.location_repository import LocationRepository
from .repositories.category_repository import CategoryRepository
from .repositories.group_repository import GroupRepository
from .repositories.entity_repository import EntityRepository
from .services.ticket_service import TicketService


class GLPIService:

    def __init__(self):

        self.users = UserRepository()
        self.chatbot = ChatbotRepository()

        # consultas SQL
        self.tickets = TicketRepository()

        # criação via REST
        self.ticket_service = TicketService()

        self.locations = LocationRepository()
        self.categories = CategoryRepository()
        self.groups = GroupRepository()
        self.entities = EntityRepository()

    # Usuários
    def identify_user(self, phone):

        mapping = self.chatbot.find_by_phone(phone)

        if not mapping:
            print("[IDENTIFY] vínculo não encontrado")
            return None

        user = self.users.find_by_id(mapping["users_id"])

        if not user:
            print("[IDENTIFY] usuário não encontrado")
            return None

        return user

    def search_user(self, text):
        return self.users.search(text)

    def link_phone(self, requester, phone):
        self.chatbot.link_phone(requester.id, phone)

    # Chamados
    def get_open_tickets(self, requester):
        return self.tickets.find_open_by_requester(requester.id)

    def create_ticket(self, ticket):
        return self.ticket_service.create(ticket)

   # Metadata
    def get_location(self, requester):

        if requester.location_id:
            return self.locations.find_by_id(requester.location_id)

    def get_group(self, requester):

        if requester.group_id:
            return self.groups.find_by_id(requester.group_id)

    def get_entity(self, requester):

        if requester.entity_id:
            return self.entities.find_by_id(requester.entity_id)

    def get_default_category(self):
        return self.categories.find_by_id(47)
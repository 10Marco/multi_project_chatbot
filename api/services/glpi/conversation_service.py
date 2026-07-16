from core.state_manager import StateManager
from services.glpi.glpi_service import GLPIService
from dataclasses import dataclass, field

# replies setados
@dataclass
class Reply:

    type: str

    data: dict = field(default_factory=dict)

    @classmethod
    def text(cls, message):

        return cls(

            type="text",

            data={

                "text": message

            }

        )

    @classmethod
    def image(cls, image, caption=None):

        return cls(

            type="image",

            data={

                "image": image,

                "caption": caption

            }

        )

    @classmethod
    def document(cls, document, caption=None):

        return cls(

            type="document",

            data={

                "document": document,

                "caption": caption

            }

        )

    @classmethod
    def buttons(cls, text, buttons):

        return cls(

            type="buttons",

            data={

                "text": text,

                "buttons": buttons

            }

        )

    @classmethod
    def list(cls, title, options):

        return cls(

            type="list",

            data={

                "title": title,

                "options": options

            }

        )
    


YES = {"sim", "s", "ok", "confirmar"}
NO = {"não", "nao", "n", "cancelar"}


class ConversationService:

    def __init__(self):

        self.state = StateManager()

        self.glpi = GLPIService()

    # helpers 
    def goto(self, conversation, sender, step):

        conversation.step = step

        self.state.save(sender, conversation)

    # conversation steps: 1 // etapas da conversa 1
    def start(self, conversation, sender, message, payload=None):

        user = self.glpi.identify_user(sender)

        if user:

            conversation.ticket.requester = user

            self.goto(
                conversation,
                sender,
                "awaiting_description"
            )

            return Reply.text(f"Olá {user.firstname or user.name}!\n\nDescreva o problema.")

        self.goto(
            conversation,
            sender,
            "awaiting_name"
        )

        return Reply.text(
            "Olá! Bem-vindo ao serviço de suporte da "
            "Diretoria de Desenvolvimento e Proteção de Dados.\n\n"
            "Informe seu nome completo ou matrícula."
        )

    # conversation steps: 2 // etapas da conversa 2
    def awaiting_name(self, conversation, sender, message, payload=None):

        users = self.glpi.search_user(message)

        if not users:

            return Reply.text(
                "Não encontrei nenhum usuário.\n"
                "Informe novamente seu nome completo ou matrícula."
            )

        if len(users) == 1:

            user = users[0]

            conversation.ticket.requester = user

            self.glpi.link_phone(user, sender)

            self.goto(
                conversation,
                sender,
                "awaiting_description"
            )

            return Reply.text(
                f"Olá {user.firstname or user.name}!\n\n"
                "Descreva o problema."
            )

        conversation.context["users"] = users

        self.goto(
            conversation,
            sender,
            "choosing_user"
        )

        response = "Encontrei estes usuários:\n\n"

        for i, user in enumerate(users, start=1):

            response += f"{i}. {user.firstname} {user.realname}\n"

        response += "\nDigite o número correspondente."

        return Reply.text(response)
    
    # conversation steps: 3 // etapas da conversa 3
    def choosing_user(self, conversation, sender, message, payload=None):

        users = conversation.context.get("users", [])

        if not message.isdigit():

            return Reply.text("Informe apenas o número da opção.")

        index = int(message) - 1

        if index < 0 or index >= len(users):

            return Reply.text("Opção inválida.")

        user = users[index]

        conversation.ticket.requester = user

        self.glpi.link_phone(user, sender)

        conversation.context.clear()

        self.goto(
            conversation,
            sender,
            "awaiting_description"
        )

        return Reply.text(
            f"Olá {user.firstname or user.name}!\n\n"
            "Descreva o problema."
        )

    # conversation steps: 4 // etapas da conversa 4
    def awaiting_description(self, conversation, sender, message, payload=None):

        conversation.ticket.description = message

        conversation.ticket.attachments.clear()

        self.goto(
            conversation,
            sender,
            "ask_attachment"
        )

        return Reply.text("Deseja anexar algum arquivo? (sim/não)")


    # conversation steps: 5 // etapas da conversa 5
    def ask_attachment(self, conversation, sender, message, payload=None):

        msg = message.lower().strip()

        if msg in YES:

            self.goto(
                conversation,
                sender,
                "waiting_attachment"
            )

            return Reply.text("Envie o arquivo.")

        if msg in NO:

            self.goto(
                conversation,
                sender,
                "confirm_ticket"
            )

            return Reply.text("Deseja confirmar a abertura do chamado? (sim/não)")

        return Reply.text("Responda apenas sim ou não.")

    # conversation steps: 6 // etapas da conversa 6
    def waiting_attachment(self, conversation, sender, message, payload=None):

        if not payload or not payload.get("media"):

            return Reply.text("Não recebi nenhum arquivo.")

        conversation.ticket.attachments.append(payload)

        self.goto(
            conversation,
            sender,
            "ask_more_attachments"
        )

        return Reply.text("Arquivo recebido.\nDeseja enviar outro? (sim/não)")

    # conversation steps: 7 // etapas da conversa 7
    def ask_more_attachments(self, conversation, sender, message, payload=None):

        msg = message.lower().strip()

        if msg in YES:

            self.goto(
                conversation,
                sender,
                "waiting_attachment"
            )

            return Reply.text("Envie o próximo arquivo.")

        if msg in NO:

            self.goto(
                conversation,
                sender,
                "confirm_ticket"
            )

            return Reply.text("Deseja confirmar a abertura do chamado? (sim/não)")

        return Reply.text("Responda apenas sim ou não.")

    # conversation steps: 8 // etapas da conversa 8
    def confirm_ticket(self, conversation, sender, message, payload=None):

        msg = message.lower().strip()

        if msg in NO:

            self.state.clear(sender)

            return Reply.text("Chamado cancelado.")

        if msg not in YES:

            return Reply.text("Responda apenas sim ou não.")

        ticket_id = self.glpi.create_ticket(
            conversation.ticket
        )

        self.state.clear(sender)

        return Reply.text (
            f"Chamado criado com sucesso!\n"
            f"Número {ticket_id}"
        )

    # conversation steps: 8 // etapas da conversa 8
    def handle(self, sender, message, payload=None):

        conversation = self.state.get(sender)

        step = conversation.step or "start"

        handlers = {

            "start": self.start,

            "awaiting_name": self.awaiting_name,

            "choosing_user": self.choosing_user,

            "awaiting_description": self.awaiting_description,

            "ask_attachment": self.ask_attachment,

            "waiting_attachment": self.waiting_attachment,

            "ask_more_attachments": self.ask_more_attachments,

            "confirm_ticket": self.confirm_ticket,

        }

        return handlers[step](
            conversation,
            sender,
            message,
            payload
        )
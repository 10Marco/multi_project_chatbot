from core.state_manager import StateManager
from services.glpi.glpi_service import GLPIService
from dataclasses import dataclass, field
from services.glpi.models.reply import Reply
from utils.constants import YES, NO


class ConversationService:

    def __init__(self):
        self.state = StateManager()
        self.glpi = GLPIService()
      
    # menu constants     
    MENU_TEXT = (
        "O que deseja fazer?\n\n"
        "1️⃣ Abrir chamado\n"
        "2️⃣ Ver meus chamados\n"
        "3️⃣ Atualizar meus dados"
    )    

    # helpers
    def goto(self, conversation, sender, step):
        conversation.step = step
        self.state.save(sender, conversation)
        
        

    #handlers
    def handle(self, sender, message, payload=None):

        command = (message or "").lower().strip()

        if command in (
            "menu",
            "inicio",
            "reiniciar",
            "start",
            "recomeçar",
            "recomecar"
        ):
            self.state.clear(sender)
            conversation = self.state.get(sender)

            return self.start(
                conversation,
                sender,
                "",
                payload
            )

        if command in (
            "cancelar",
            "cancel",
            "sair"
        ):
            self.state.clear(sender)

            return Reply.text(
                "Atendimento cancelado.\n\n"
                "Envie qualquer mensagem para iniciar novamente."
            )

        conversation = self.state.get(sender)

        step = conversation.step or "start"

        handlers = {
            "start": self.start,
            "awaiting_name": self.awaiting_name,
            "choosing_user": self.choosing_user,
            "choose_ticket": self.choose_ticket,
            "main_menu": self.main_menu,
            "choose_category": self.choose_category,
            "awaiting_description": self.awaiting_description,
            "ask_attachment": self.ask_attachment,
            "waiting_attachment": self.waiting_attachment,
            "ask_more_attachments": self.ask_more_attachments,
            "confirm_ticket": self.confirm_ticket,
        }

        handler = handlers.get(step)

        if not handler:

            self.state.clear(sender)

            conversation = self.state.get(sender)

            return self.start(
                conversation,
                sender,
                "",
                payload
            )

        return handler(
            conversation,
            sender,
            message,
            payload
        )
        
        

    # main menu
    def main_menu(self, conversation, sender, message, payload=None):

        match message.strip():

            case "1":
                self.goto(
                    conversation,
                    sender,
                    "choose_category"
                )
                return Reply.text(
                    "Selecione a categoria:\n\n"
                    "1. Alteração de senha\n"
                    "2. Alteração de dados\n"
                    "3. Auto não encontrado\n"
                    "4. Manutenção do sistema\n"
                    "5. Sugestão evolutiva\n"
                    "6. Outros"
                )

            case "2":
                tickets = self.glpi.get_open_tickets(
                    conversation.ticket.requester
                )   
                if not tickets:
                    return Reply.text(
                        "Você não possui chamados em aberto."
                    )
                    
                conversation.context["tickets"] = tickets
                self.goto(
                    conversation,
                    sender,
                    "choose_ticket"
                )
                
                texto = "Seus chamados em aberto:\n\n"
                for i, ticket in enumerate(tickets, start=1):
                    texto += (
                        f"{i}. #{ticket['id']} - "
                        f"{ticket['name']}\n"
                    )

                texto += (
                    "\nDigite o número do chamado para enviar uma atualização.\n\n"
                    "Ou digite MENU para voltar."
                )    
                return Reply.text(texto)

            case "3":
                return Reply.text(
                    "Em breve você poderá atualizar seus dados."
                )

            case _:
                return Reply.text(
                    "Escolha uma opção válida."
                )

    # categories
    def choose_category(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        CATEGORY_MAP = {
            "1": {
                "id": 51,
                "title": "[DEV] Alteração de senha"
            },
            
            "2": {
                "id": 52,
                "title": "[DEV] Alteração de dados"
            },

            "3": {
                "id": 53,
                "title": "[DEV] Auto não encontrado"
            },

            "4": {
                "id": 54,
                "title": "[DEV] Manutenção do sistema"
            },

            "5": {
                "id": 55,
                "title": "[DEV] Sugestão evolutiva"
            },

            "6": {
                "id": 56,
                "title": "[DEV] Outros"
            }

        }

        option = CATEGORY_MAP.get(message)

        if not option:

            return Reply.text(
                "Escolha uma categoria válida."
            )

        conversation.ticket.category = option["id"]

        conversation.ticket.title = option["title"]

        self.goto(
            conversation,
            sender,
            "awaiting_description"
        )

        return Reply.text(

            "Descreva sua solicitação com o máximo de detalhes possível.\n\n"

            "Se houver mensagens de erro, informe exatamente o texto exibido.\n\n"

            "Caso o problema envolva um Auto de Infração, informe o número do Auto e se possível, o PDF."

        )
        
    def choose_ticket(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        tickets = conversation.context.get("tickets", [])

        if not message.isdigit():
            return Reply.text(
                "Informe apenas o número da opção."
            )

        index = int(message) - 1

        if index < 0 or index >= len(tickets):
            return Reply.text(
                "Opção inválida."
            )

        ticket = tickets[index]

        conversation.context["ticket_followup"] = ticket

        self.goto(
            conversation,
            sender,
            "awaiting_followup"
        )

        return Reply.text(
            f"Você selecionou o chamado #{ticket['id']}.\n\n"
            "Digite a atualização que deseja adicionar."
        )
        
        
        
        
     # conversation steps: 1 // etapas da conversa 1
    def start(self, conversation, sender, message, payload=None):
        user = self.glpi.identify_user(sender)

        if user:
            conversation.ticket.requester = user
            self.goto(
                conversation,
                sender,
                "main_menu"
            )
            return Reply.text(
                f"Olá {(user.firstname or user.name).title()}!\n\n"
                f"{self.MENU_TEXT}"
            )

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
                "main_menu"
            )

            return Reply.text(
                f"Olá {(user.firstname or user.name).title()}!\n\n"
                f"{self.MENU_TEXT}"
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
            "main_menu"
        )

        return Reply.text(
            f"Olá {(user.firstname or user.name).title()}!\n\n"
            f"{self.MENU_TEXT}"
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
    def waiting_attachment(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        attachment = None

        if payload:
            attachment = payload.get("attachment")

        if not attachment:
            return Reply.text(
                "Não recebi nenhum arquivo."
            )

        conversation.ticket.attachments.append(attachment)
        attachment = payload.get("attachment")
        print(type(attachment))
        print(attachment)
        

        self.goto(
            conversation,
            sender,
            "ask_more_attachments"
        )

        return Reply.text(
            "Arquivo recebido.\n"
            "Deseja enviar outro? (sim/não)"
        )

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

        return Reply.text(
            f"Chamado criado com sucesso!\n"
            f"Número {ticket_id}"
        )
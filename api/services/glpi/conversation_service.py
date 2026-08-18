from core.state_manager import StateManager
from services.glpi.glpi_service import GLPIService
from services.glpi.models.reply import Reply
from utils.constants import YES, NO
from utils.logger import debug
from datetime import date

class ConversationService:

    def __init__(self):

        self.state = StateManager()
        self.glpi = GLPIService()


    MENU_TEXT = (
        "O que deseja fazer?\n\n"
        "1️⃣ Abrir chamado\n"
        "2️⃣ Ver meus chamados\n"
        "3️⃣ Consultar folha de ponto"
    )


    def goto(self, conversation, sender, step):

        conversation.step = step

        self.state.save(
            sender,
            conversation
        )

    def handle(self, sender, message, payload=None):

        command = (
            message or ""
        ).lower().strip()

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

            debug(
                "[CONVERSATION] step inválido: %s",
                step
            )

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

    def start(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        user = self.glpi.identify_user(sender)

        if not user:

            return Reply.text(
                "Seu número de telefone não está cadastrado "
                "para utilização deste serviço.\n\n"
                "Entre em contato com seu Gestor ou com "
                "a Subsecretaria de Tecnologia."
            )

        conversation.ticket.requester = user

        debug(
            "[CONVERSATION] usuário identificado: "
            "%s | id=%s | tipo=%s | id_sifop=%s",
            user.name,
            user.id,
            user.tipo,
            user.id_sifop
        )

        self.goto(
            conversation,
            sender,
            "main_menu"
        )

        return Reply.text(
            f"Olá {(user.firstname or user.name).title()}!\n\n"
            f"{self.MENU_TEXT}"
        )

    def main_menu(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

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
                    "2. Auto não encontrado\n"
                    "3. Manutenção do sistema\n"
                    "4. Sugestão evolutiva\n"
                    "5. Outros"
                )

            case "2":

                tickets = self.glpi.get_open_tickets(
                    conversation.ticket.requester
                )

                if not tickets:

                    return Reply.text(
                        "Você não possui chamados em aberto."
                    )

                texto = (
                    "📂 *Seus chamados em aberto*\n\n"
                )

                for i, ticket in enumerate(
                    tickets,
                    start=1
                ):

                    texto += (
                        f"{i}️⃣ *#{ticket.id}*\n"
                        f"{ticket.name}\n"
                        f"🔗 {ticket.url(self.glpi.web_url)}\n\n"
                    )

                texto += (
                    "Digite *MENU* para voltar "
                    "ao menu principal."
                )

                return Reply.text(texto)

            case "3":

                return self.gerar_folha(
                    conversation,
                    sender
                )

            case _:

                return Reply.text(
                    "Escolha uma opção válida:\n\n"
                    f"{self.MENU_TEXT}"
                )


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
                "id": 53,
                "title": "[DEV] Auto não encontrado"
            },

            "3": {
                "id": 54,
                "title": "[DEV] Manutenção do sistema"
            },

            "4": {
                "id": 55,
                "title": "[DEV] Sugestão evolutiva"
            },

            "5": {
                "id": 56,
                "title": "[DEV] Outros"
            }
        }

        option = CATEGORY_MAP.get(
            message
        )

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
            "Descreva sua solicitação com o máximo "
            "de detalhes possível.\n\n"
            "Se houver mensagens de erro, informe "
            "exatamente o texto exibido.\n\n"
            "Caso o problema envolva um Auto de Infração, "
            "informe o número do Auto e, se possível, o PDF."
        )


    def awaiting_description(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        conversation.ticket.description = message

        conversation.ticket.attachments.clear()

        self.goto(
            conversation,
            sender,
            "ask_attachment"
        )

        return Reply.text(
            "Deseja anexar algum arquivo? (sim/não)"
        )

    def ask_attachment(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        msg = message.lower().strip()

        if msg in YES:

            self.goto(
                conversation,
                sender,
                "waiting_attachment"
            )

            return Reply.text(
                "Envie o arquivo."
            )

        if msg in NO:

            self.goto(
                conversation,
                sender,
                "confirm_ticket"
            )

            return Reply.text(
                "Deseja confirmar a abertura "
                "do chamado? (sim/não)"
            )

        return Reply.text(
            "Responda apenas sim ou não."
        )

 
    def waiting_attachment(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        attachment = None

        if payload:

            attachment = payload.get(
                "attachment"
            )

        if not attachment:

            return Reply.text(
                "Não recebi nenhum arquivo."
            )

        conversation.ticket.attachments.append(
            attachment
        )

        debug(
            "Attachment recebido: %s | %s",
            type(attachment),
            attachment
        )

        self.goto(
            conversation,
            sender,
            "ask_more_attachments"
        )

        return Reply.text(
            "Arquivo recebido.\n"
            "Deseja enviar outro? (sim/não)"
        )

    def ask_more_attachments(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        msg = message.lower().strip()

        if msg in YES:

            self.goto(
                conversation,
                sender,
                "waiting_attachment"
            )

            return Reply.text(
                "Envie o próximo arquivo."
            )

        if msg in NO:

            self.goto(
                conversation,
                sender,
                "confirm_ticket"
            )

            return Reply.text(
                "Deseja confirmar a abertura "
                "do chamado? (sim/não)"
            )

        return Reply.text(
            "Responda apenas sim ou não."
        )

    def confirm_ticket(
        self,
        conversation,
        sender,
        message,
        payload=None
    ):

        msg = message.lower().strip()

        if msg in NO:

            self.state.clear(sender)

            return Reply.text(
                "Chamado cancelado."
            )

        if msg not in YES:

            return Reply.text(
                "Responda apenas sim ou não."
            )

        ticket_id = self.glpi.create_ticket(
            conversation.ticket
        )

        self.state.clear(sender)

        return Reply.text(
            f"Chamado criado com sucesso!\n"
            f"Número {ticket_id}"
        )
        
    def gerar_folha(self, conversation, sender):
        requester = conversation.ticket.requester

        sifop_data = self.glpi.get_sifop_data(requester)

        if not sifop_data:
            return Reply.error(
                "Seu usuário não possui vínculo cadastrado no SIFOP."
            )

        tipo = sifop_data["tipo"].lower()
        id_sifop = sifop_data["id_sifop"]

        hoje = date.today()
        mes = hoje.month

        nome_mes = [
            "",
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro"
        ][mes]

        filename = (
            f"FI - {requester.name} - {nome_mes}.pdf"
        )

        self.state.clear(sender)

        return Reply.sifop_folha(
            tipo=tipo,
            id=id_sifop,
            mes=mes,
            filename=filename
        )
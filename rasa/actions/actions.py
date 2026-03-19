class ActionCriarChamado(Action):
    def name(self):
        return "action_criar_chamado"

    def run(self, dispatcher, tracker, domain):

        data = {
            "usuario_sei": tracker.get_slot("usuario_sei"),
            "tipo_problema": tracker.get_slot("tipo_problema"),
            "descricao": tracker.get_slot("descricao"),
            "anexar": tracker.get_slot("anexar")
        }

        response = requests.post(
            "http://middleware:8000/ticket",
            json=data
        )

        ticket = response.json().get("ticket_id", "N/A")

        dispatcher.utter_message(
            text=f"✅ Chamado criado com sucesso!\nNúmero: {ticket}"
        )

        return []
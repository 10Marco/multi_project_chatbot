from fastapi import FastAPI
import requests
import os
import time

from services.glpi import criar_ticket_glpi
from services.garagem import criar_orcamento
from services.loja import criar_pedido
from redis_client import r

RASA_URL = "http://rasa:5005/webhooks/rest/webhook"

app = FastAPI()


def get_projeto(sender: str):
    if sender == os.getenv("GLPI_NUMBER"):
        return "GLPI"
    elif sender == os.getenv("GARAGEM_NUMBER"):
        return "GARAGEM"
    elif sender == os.getenv("LOJA_NUMBER"):
        return "LOJA"
    return os.getenv("PROJECT_DEFAULT", "GLPI")


# 🔥 retry para o Rasa
def call_rasa(payload, retries=5):
    for i in range(retries):
        try:
            resp = requests.post(
                RASA_URL,
                json=payload,
                timeout=5
            )
            return resp.json()
        except Exception as e:
            print(f"🔁 Tentativa {i+1} falhou:", e)
            time.sleep(2)

    return [{"text": "Erro ao conectar com o Rasa"}]


@app.post("/whatsapp")
def whatsapp(payload: dict):
    sender = payload.get("from") or payload.get("sender")
    message = (payload.get("message") or payload.get("body") or "").lower()

    projeto = get_projeto(sender)

    print(f"📥 [{projeto}] {sender}: {message}")

    state_key = f"user:{sender}:state"
    state = r.get(state_key)

    # 🔥 CANCELAMENTO GLOBAL
    if state == "aguardando_confirmacao" and message in ["não", "nao"]:
        r.delete(state_key)
        return {
            "to": sender,
            "messages": ["❌ Chamado cancelado."]
        }

    # 🔥 CHAMAR RASA (AGORA SIM)
    rasa_data = call_rasa({
        "sender": sender,
        "message": message
    })

    responses = []

    for r_item in rasa_data:
        if "text" in r_item:
            responses.append(r_item["text"])

        if r_item.get("custom", {}).get("action"):
            action = r_item["custom"]["action"]

            # salvar estado
            if action == "create_ticket":
                r.set(state_key, "aguardando_confirmacao")

            if action == "create_ticket" and projeto == "GLPI":
                ticket = criar_ticket_glpi(sender, message)
                r.delete(state_key)

                responses.append(f"✅ Chamado criado! Nº {ticket}")

            elif action == "create_budget" and projeto == "GARAGEM":
                orcamento = criar_orcamento(sender, message)
                responses.append(f"🚗 Orçamento: {orcamento}")

            elif action == "create_order" and projeto == "LOJA":
                pedido = criar_pedido(sender, message)
                responses.append(f"🛒 Pedido: {pedido}")

    # 🔥 FALLBACK FINAL
    if not responses:
        print("⚠️ Rasa não respondeu")
        responses.append("🤖 Não entendi. Digite 'oi' para começar.")

    return {
        "to": sender,
        "messages": responses
    }
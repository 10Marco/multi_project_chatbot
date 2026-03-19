import requests
from config import GLPI_URL, USER_TOKEN, APP_TOKEN

def get_session():
    r = requests.post(
        f"{GLPI_URL}/initSession",
        headers={
            "Authorization": f"user_token {USER_TOKEN}",
            "App-Token": APP_TOKEN
        },
        verify=False
    )

    return r.json()["session_token"]


def create_ticket(session, usuario, descricao):
    payload = {
        "input": {
            "name": f"Chamado - {usuario}",
            "content": descricao,
            "itilcategories_id": 1
        }
    }

    r = requests.post(
        f"{GLPI_URL}/Ticket",
        headers={
            "Session-Token": session,
            "App-Token": APP_TOKEN,
            "Content-Type": "application/json"
        },
        json=payload,
        verify=False
    )

    return r.json()["id"]
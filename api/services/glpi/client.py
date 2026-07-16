import requests

from config import GLPI_URL, APP_TOKEN
from services.glpi.session import get_session


def criar_ticket_glpi(ticket):

    headers = {
        "App-Token": APP_TOKEN,
        "Session-Token": get_session()
    }

    response = requests.post(
        f"{GLPI_URL}/Ticket",
        json=ticket,
        headers=headers
    )

    print("========== GLPI ==========")
    print(response.status_code)
    print(response.text)
    print("==========================")

    response.raise_for_status()

    return response.json()["id"]
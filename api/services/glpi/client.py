import json
import requests

from config import GLPI_URL, APP_TOKEN
from services.glpi.session import get_session


def _headers():
    return {
        "App-Token": APP_TOKEN,
        "Session-Token": get_session()
    }


def create_ticket_glpi(ticket):

    response = requests.post(
        f"{GLPI_URL}/Ticket",
        json=ticket,
        headers=_headers()
    )

    print("========== GLPI ==========")
    print(response.status_code)
    print(response.text)
    print("==========================")

    response.raise_for_status()

    return response.json()["id"]


def upload_document_glpi(ticket_id, attachment):

    manifest = {
        "input": {
            "name": attachment.filename,
            "_filename": [attachment.filename],
            "itemtype": "Ticket",
            "items_id": ticket_id
        }
    }

    with open(attachment.local_path, "rb") as file:
        response = requests.post(
            f"{GLPI_URL}/Document",
            headers=_headers(),
            files={
                "uploadManifest": (
                    None,
                    json.dumps(manifest),
                    "application/json"
                ),
                "filename": (
                    attachment.filename,
                    file,
                    attachment.mimetype
                )
            }
        )

    print("======= DOCUMENT =======")
    print(response.status_code)
    print(response.headers)
    print(response.text)

    try:
        print(response.json())
    except Exception:
        pass
    print("========================")
    response.raise_for_status()

    return response.json()["id"]


def attach_document_to_ticket(ticket_id, document_id):

    payload = {
        "input": {
            "documents_id": document_id,
            "items_id": ticket_id,
            "itemtype": "Ticket"
        }
    }

    response = requests.post(
        f"{GLPI_URL}/Document_Item",
        json=payload,
        headers=_headers()
    )

    print("===== DOCUMENT ITEM =====")
    print(response.status_code)
    print(response.text)
    print("=========================")

    response.raise_for_status()
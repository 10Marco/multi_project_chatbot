import json
import requests

from config import GLPI_URL, APP_TOKEN
from services.glpi.session import get_session
from utils.logger import debug


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

    debug(
        "GLPI create ticket status=%s body=%s",
        response.status_code,
        response.text,
    )

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

    debug(
        "GLPI upload document status=%s headers=%s body=%s",
        response.status_code,
        dict(response.headers),
        response.text,
    )
    response.raise_for_status()

    return response.json()["id"]

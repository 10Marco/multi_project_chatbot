import requests

from redis_client import r
from config import GLPI_URL, APP_TOKEN, USER_TOKEN

SESSION_KEY = "glpi:session"
TTL = 1800  


def get_session():

    token = r.get(SESSION_KEY)

    if token:
        return token

    headers = {
        "App-Token": APP_TOKEN,
        "Authorization": f"user_token {USER_TOKEN}"
    }

    response = requests.get(
        f"{GLPI_URL}/initSession",
        headers=headers
    )

    response.raise_for_status()

    token = response.json()["session_token"]

    r.set(
        SESSION_KEY,
        token,
        ex=TTL
    )

    return token
import os
import traceback

from utils.environment import DEBUG
from utils.logger import exception


def debug_reply(exc: Exception):
    if not DEBUG:
        return {
            "type": "text",
            "text": "Erro interno."
        }

    debug_console(exc)

    tb = traceback.extract_tb(exc.__traceback__)
    last = tb[-1]
    return {
        "type": "text",
        "text": (
            "Erro interno.\n\n"
            f"Arquivo: {os.path.basename(last.filename)}\n"
            f"Linha: {last.lineno}\n"
            f"Função: {last.name}\n\n"
            f"{type(exc).__name__}\n"
            f"{exc}"
        )
    }


def debug_console(exc: Exception):
    exception("Exceção não tratada", exc_info=exc)

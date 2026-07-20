import os
import traceback

def debug_reply(exc: Exception):

    debug_console(exc)

    tb = traceback.extract_tb(exc.__traceback__)
    last = tb[-1]
    return {
        "type": "text",
        "text": (
            "❌ Erro interno.\n\n"
            f"Arquivo: {os.path.basename(last.filename)}\n"
            f"Linha: {last.lineno}\n"
            f"Função: {last.name}\n\n"
            f"{type(exc).__name__}\n"
            f"{exc}"
        )
    }


def debug_console(exc: Exception):
    print("\n========== EXCEPTION ==========")
    traceback.print_exc()
    print("===============================\n")
import os


def get_projeto(sender: str):
    mapping = {
        os.getenv("GLPI_NUMBER"): "GLPI",
        os.getenv("GARAGEM_NUMBER"): "GARAGEM",
        os.getenv("LOJA_NUMBER"): "LOJA",
    }

    return mapping.get(sender, os.getenv("PROJECT_DEFAULT", "GLPI"))
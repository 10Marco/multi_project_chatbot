import os

PROJECTS = {
    os.getenv("GLPI_NUMBER"): "GLPI",
    os.getenv("GARAGEM_NUMBER"): "GARAGEM",
    os.getenv("LOJA_NUMBER"): "LOJA",
}


def get_project(sender):
    return PROJECTS.get(
        sender,
        os.getenv("PROJECT_DEFAULT", "GLPI")
    )
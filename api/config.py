import os

from dotenv import load_dotenv

load_dotenv()

# =====================================
# GLPI API
# =====================================

GLPI_URL = os.getenv("GLPI_URL")
USER_TOKEN = os.getenv("USER_TOKEN")
APP_TOKEN = os.getenv("APP_TOKEN")

# =====================================
# GLPI DATABASE
# =====================================

GLPI_DB_HOST = os.getenv("GLPI_DB_HOST")
GLPI_DB_PORT = int(os.getenv("GLPI_DB_PORT", 3306))
GLPI_DB_NAME = os.getenv("GLPI_DB_NAME")
GLPI_DB_USER = os.getenv("GLPI_DB_USER")
GLPI_DB_PASSWORD = os.getenv("GLPI_DB_PASSWORD")

# =====================================
# CHATBOT DATABASE
# =====================================

CHATBOT_DB_PORT = int(os.getenv("CHATBOT_DB_PORT", 3306))
CHATBOT_DB_HOST = os.getenv("CHATBOT_DB_HOST")
CHATBOT_DB_NAME = os.getenv("CHATBOT_DB_NAME")
CHATBOT_DB_USER = os.getenv("CHATBOT_DB_USER")
CHATBOT_DB_PASSWORD = os.getenv("CHATBOT_DB_PASSWORD")
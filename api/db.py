import pymysql

from config import (
    GLPI_DB_HOST,
    GLPI_DB_PORT,
    GLPI_DB_NAME,
    GLPI_DB_USER,
    GLPI_DB_PASSWORD,

    CHATBOT_DB_HOST,
    CHATBOT_DB_PORT,
    CHATBOT_DB_NAME,
    CHATBOT_DB_USER,
    CHATBOT_DB_PASSWORD
)


def _connect(host, port, database, user, password):

    return pymysql.connect(

        host=host,

        port=port,

        database=database,

        user=user,

        password=password,

        charset="utf8mb4",

        cursorclass=pymysql.cursors.DictCursor,

        autocommit=True

    )


def get_glpi_connection():

    return _connect(

        GLPI_DB_HOST,

        GLPI_DB_PORT,

        GLPI_DB_NAME,

        GLPI_DB_USER,

        GLPI_DB_PASSWORD

    )

def get_chatbot_connection():

    return _connect(

        CHATBOT_DB_HOST,

        CHATBOT_DB_PORT,

        CHATBOT_DB_NAME,

        CHATBOT_DB_USER,

        CHATBOT_DB_PASSWORD

    )
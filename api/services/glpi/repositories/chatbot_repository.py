from db import get_chatbot_connection

from services.glpi.repositories.base_repository import BaseRepository
from utils.logger import debug


class ChatbotRepository(BaseRepository):

    def __init__(self):
        super().__init__(get_chatbot_connection)

    def find_by_phone(self, phone: str):

        debug("[CHATBOT_DB] procurando %s", phone)

        sql = """
        SELECT *
        FROM chatbot_glpi
        WHERE whatsapp=%s
          AND active=1
        LIMIT 1
        """

        return self.fetch_one(sql, (phone,))

    def link_phone(self, users_id: int, phone: str):

        debug("[CHATBOT_DB] vinculando %s -> %s", phone, users_id)

        sql = """
        INSERT INTO chatbot_glpi
        (
            users_id,
            whatsapp,
            active,
            created_at,
            updated_at
        )
        VALUES
        (
            %s,
            %s,
            1,
            NOW(),
            NOW()
        )
        ON DUPLICATE KEY UPDATE
            users_id=VALUES(users_id),
            whatsapp=VALUES(whatsapp),
            active=1,
            updated_at=NOW()
        """

        self.execute(
            sql,
            (
                users_id,
                phone
            )
        )

    def find_by_user_id(self, users_id: int):

        sql = """
        SELECT
            id,
            users_id,
            whatsapp,
            active,
            created_at,
            updated_at,
            id_sifop,
            tipo
        FROM chatbot_glpi
        WHERE users_id=%s
        AND active=1
        LIMIT 1
        """

        return self.fetch_one(sql, (users_id,))
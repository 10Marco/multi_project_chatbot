from db import get_chatbot_connection

from services.glpi.repositories.base_repository import BaseRepository


class ChatbotRepository(BaseRepository):

    def __init__(self):
        super().__init__(get_chatbot_connection)

    def find_by_phone(self, phone: str):

        print(f"[CHATBOT_DB] procurando {phone}")

        sql = """
        SELECT *
        FROM chatbot_glpi
        WHERE whatsapp=%s
          AND active=1
        LIMIT 1
        """

        return self.fetch_one(sql, (phone,))

    def link_phone(self, users_id: int, phone: str):

        print(f"[CHATBOT_DB] vinculando {phone} -> {users_id}")

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

    def unlink_phone(self, phone: str):

        sql = """
        UPDATE chatbot_glpi
        SET
            active=0,
            updated_at=NOW()
        WHERE whatsapp=%s
        """

        self.execute(sql, (phone,))

    def update_phone(self, users_id: int, phone: str):

        sql = """
        UPDATE chatbot_glpi
        SET
            whatsapp=%s,
            updated_at=NOW()
        WHERE users_id=%s
        """

        self.execute(
            sql,
            (
                phone,
                users_id
            )
        )
from db import get_chatbot_connection


class ChatbotRepository:


    def find_by_phone(self, phone: str):

        print(f"[CHATBOT_DB] procurando {phone}")

        sql = """
        SELECT *
        FROM chatbot_glpi
        WHERE whatsapp=%s
          AND active=1
        LIMIT 1

        """

        with get_chatbot_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    sql,
                    (phone,)
                )

                return cursor.fetchone()


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

        with get_chatbot_connection() as conn:

            with conn.cursor() as cursor:
                cursor.execute(
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

        with get_chatbot_connection() as conn:

            with conn.cursor() as cursor:
                cursor.execute(
                    sql,
                    (phone,)
                )


    def update_phone(self, users_id: int, phone: str):

        sql = """
        UPDATE chatbot_glpi
        SET
            whatsapp=%s,
            updated_at=NOW()
        WHERE users_id=%s

        """

        with get_chatbot_connection() as conn:

            with conn.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        phone,
                        users_id
                    )
                )
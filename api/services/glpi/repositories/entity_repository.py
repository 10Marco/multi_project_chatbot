from db import get_glpi_connection

from services.glpi.repositories.base_repository import BaseRepository


class EntityRepository(BaseRepository):

    def __init__(self):
        super().__init__(get_glpi_connection)

    def find_by_id(self, entity_id):

        sql = """
        SELECT
            id,
            name,
            completename,
            entities_id,
            level,
            registration_number,
            email,
            phonenumber
        FROM glpi_entities
        WHERE id=%s
        LIMIT 1
        """

        return self.fetch_one(sql, (entity_id,))

    def find_exact(self, name):

        sql = """
        SELECT
            id,
            name,
            completename
        FROM glpi_entities
        WHERE LOWER(name)=LOWER(%s)
        LIMIT 1
        """

        return self.fetch_one(sql, (name,))

    def search(self, text):

        like = f"%{text}%"

        sql = """
        SELECT
            id,
            name,
            completename,
            level
        FROM glpi_entities
        WHERE
            LOWER(
                CONCAT_WS(
                    ' ',
                    name,
                    completename
                )
            )
            LIKE LOWER(%s)
        ORDER BY
            completename
        LIMIT 20
        """

        return self.fetch_all(sql, (like,))

    def list(self):

        sql = """
        SELECT
            id,
            name,
            completename
        FROM glpi_entities
        ORDER BY
            completename
        """

        return self.fetch_all(sql)
from db import get_glpi_connection

from services.glpi.repositories.base_repository import BaseRepository


class GroupRepository(BaseRepository):

    def __init__(self):
        super().__init__(get_glpi_connection)

    def find_by_id(self, group_id):

        sql = """
        SELECT
            id,
            name,
            completename,
            entities_id,
            groups_id,
            level,
            is_requester,
            is_assign,
            is_manager
        FROM glpi_groups
        WHERE id=%s
        LIMIT 1
        """

        return self.fetch_one(sql, (group_id,))

    def find_exact(self, name):

        sql = """
        SELECT
            id,
            name,
            completename
        FROM glpi_groups
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
        FROM glpi_groups
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
        FROM glpi_groups
        ORDER BY
            completename
        """

        return self.fetch_all(sql)

    def list_by_entity(self, entity_id):

        sql = """
        SELECT
            id,
            name,
            completename
        FROM glpi_groups
        WHERE entities_id=%s
        ORDER BY completename
        """

        return self.fetch_all(sql, (entity_id,))
from db import get_glpi_connection
from services.glpi.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):

    def __init__(self):
        super().__init__(get_glpi_connection)

    def find_by_id(self, category_id: int):

        sql = """
        SELECT
            id,
            name,
            completename,
            itilcategories_id,
            entities_id,
            level,
            is_helpdeskvisible,
            is_incident,
            is_request
        FROM glpi_itilcategories
        WHERE id=%s
        LIMIT 1
        """

        return self.fetch_one(sql, (category_id,))

    def search(self, text: str):

        sql = """
        SELECT
            id,
            name,
            completename,
            level,
            is_incident,
            is_request
        FROM glpi_itilcategories
        WHERE
            is_helpdeskvisible=1
            AND
            (
                LOWER(name) LIKE LOWER(%s)
                OR LOWER(completename) LIKE LOWER(%s)
            )
        ORDER BY
            level,
            completename
        LIMIT 20
        """

        like = f"%{text}%"

        return self.fetch_all(sql, (like, like))

    def list_visible(self):

        sql = """
        SELECT
            id,
            name,
            completename
        FROM glpi_itilcategories
        WHERE is_helpdeskvisible=1
        ORDER BY completename
        """

        return self.fetch_all(sql)

    def find_exact(self, name: str):

        sql = """
        SELECT
            id,
            name,
            completename
        FROM glpi_itilcategories
        WHERE LOWER(name)=LOWER(%s)
        LIMIT 1
        """

        return self.fetch_one(sql, (name,))
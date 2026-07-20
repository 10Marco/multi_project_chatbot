from db import get_glpi_connection

from services.glpi.repositories.base_repository import BaseRepository


class LocationRepository(BaseRepository):

    def __init__(self):
        super().__init__(get_glpi_connection)

    def find_by_id(self, location_id):

        sql = """
        SELECT
            id,
            name,
            completename,
            entities_id,
            locations_id
        FROM glpi_locations
        WHERE id=%s
        LIMIT 1
        """

        return self.fetch_one(sql, (location_id,))

    def search(self, text):

        like = f"%{text}%"

        sql = """
        SELECT
            id,
            name,
            completename
        FROM glpi_locations
        WHERE LOWER(completename)
        LIKE LOWER(%s)
        ORDER BY
            level,
            completename
        LIMIT 20
        """

        return self.fetch_all(sql, (like,))

    def list_by_entity(self, entity_id):

        sql = """
        SELECT
            id,
            name,
            completename
        FROM glpi_locations
        WHERE entities_id=%s
        ORDER BY completename
        """

        return self.fetch_all(sql, (entity_id,))
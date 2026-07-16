from db import get_glpi_connection


class LocationRepository:


    def find_by_id(self, location_id: int):

        sql = """

        SELECT

            id,

            name,

            completename,

            entities_id,

            locations_id

        FROM glpi_locations

        WHERE

            id=%s

        LIMIT 1

        """

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(

                    sql,

                    (

                        location_id,

                    )

                )

            return cursor.fetchone()


    def search(self, text: str):

        sql = """

        SELECT

            id,

            name,

            completename

        FROM glpi_locations

        WHERE

            LOWER(completename)

            LIKE LOWER(%s)

        ORDER BY

            level,

            completename

        LIMIT 20

        """

        like = f"%{text}%"

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(

                    sql,

                    (

                        like,

                    )

                )

                return cursor.fetchall()


    def list_by_entity(self, entity_id: int):

        sql = """

        SELECT

            id,

            name,

            completename

        FROM glpi_locations

        WHERE

            entities_id=%s

        ORDER BY

            completename

        """

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(

                    sql,

                    (

                        entity_id,

                    )

                )

                return cursor.fetchall()
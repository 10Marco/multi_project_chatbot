from db import get_glpi_connection


class GroupRepository:


    def find_by_id(self, group_id: int):

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

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(

                    sql,

                    (

                        group_id,

                    )

                )

                return cursor.fetchone()


    def find_exact(self, name: str):

        sql = """

        SELECT

            id,

            name,

            completename

        FROM glpi_groups

        WHERE

            LOWER(name)=LOWER(%s)

        LIMIT 1

        """

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(

                    sql,

                    (

                        name,

                    )

                )

                return cursor.fetchone()


    def search(self, text: str):

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

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(sql)

                return cursor.fetchall()


    def list_by_entity(self, entity_id: int):

        sql = """

        SELECT

            id,

            name,

            completename

        FROM glpi_groups

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
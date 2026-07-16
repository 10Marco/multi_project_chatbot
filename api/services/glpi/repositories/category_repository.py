from db import get_glpi_connection


class CategoryRepository:


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

        WHERE

            id=%s

        LIMIT 1

        """

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(

                    sql,

                    (

                        category_id,

                    )

                )

                return cursor.fetchone()


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

                LOWER(name)

                    LIKE LOWER(%s)

                OR

                LOWER(completename)

                    LIKE LOWER(%s)

            )

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

                        like

                    )

                )

                return cursor.fetchall()


    def list_visible(self):

            sql = """

            SELECT

                id,

                name,

                completename

            FROM glpi_itilcategories

            WHERE

                is_helpdeskvisible=1

            ORDER BY

                completename

            """

            with get_glpi_connection() as conn:

                with conn.cursor() as cursor:

                    cursor.execute(sql)

                    return cursor.fetchall()

    def find_exact(self, name: str):

        sql = """

        SELECT

            id,

            name,

            completename

        FROM glpi_itilcategories

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
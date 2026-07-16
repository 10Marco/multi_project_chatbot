from db import get_glpi_connection


class TicketRepository:

    def find_open_by_requester(self, user_id: int):

        sql = """

        SELECT

            t.id,

            t.name,

            t.status,

            t.priority,

            t.date,

            t.itilcategories_id,

            t.locations_id

        FROM glpi_tickets t

        INNER JOIN glpi_tickets_users tu

            ON tu.tickets_id = t.id

        WHERE

            tu.users_id = %s

            AND tu.type = 1

            AND t.is_deleted = 0

            AND t.status NOT IN (5,6)

        ORDER BY

            t.date DESC

        LIMIT 20

        """

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(sql, (user_id,))

                return cursor.fetchall()
            


    def find_last_by_requester(self, user_id: int):

        sql = """

        SELECT

            t.id,

            t.name,

            t.status,

            t.date,

            t.closedate

        FROM glpi_tickets t

        INNER JOIN glpi_tickets_users tu

            ON tu.tickets_id=t.id

        WHERE

            tu.users_id=%s

            AND tu.type=1

            AND t.is_deleted=0

        ORDER BY

            t.date DESC

        LIMIT 1

        """

    def count_open(self, user_id):
        
        sql = """

            SELECT

            COUNT(*) AS open_tickets_count

            FROM glpi_tickets t

            INNER JOIN glpi_tickets_users tu

            ON tu.tickets_id=t.id

            WHERE

            tu.users_id=%s

            AND tu.type=1

            AND t.status NOT IN (5,6)

            AND t.is_deleted=0

        """

        with get_glpi_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(sql, (user_id,))

                result = cursor.fetchone()

            return result["open_tickets_count"] if result else 0
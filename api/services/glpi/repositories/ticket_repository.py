from db import get_glpi_connection
from services.glpi.repositories.base_repository import BaseRepository
from services.glpi.models.ticket_summary import TicketSummary



class TicketRepository(BaseRepository):

    def __init__(self):
        super().__init__(get_glpi_connection)

    def find_open_by_requester(self, user_id):

        sql = """
        SELECT
            t.id,
            t.name
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

        rows = self.fetch_all(sql, (user_id,))

        return [
            TicketSummary(
                id=row["id"],
                name=row["name"]
            )
            for row in rows
        ]

    def find_last_by_requester(self, user_id):

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

        return self.fetch_one(sql, (user_id,))

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

        result = self.fetch_one(sql, (user_id,))

        return result.get("open_tickets_count", 0)

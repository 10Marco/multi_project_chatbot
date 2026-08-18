from db import get_glpi_connection

from utils.text import normalize

from services.glpi.models.requester import Requester
from services.glpi.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(get_glpi_connection)

    def _row_to_requester(self, row):

        if not row:
            return None

        return Requester(
            id=row["id"],
            name=row["name"],
            firstname=row["firstname"],
            realname=row["realname"],
            registration=row.get("registration_number"),
            phone=row["phone"],
            mobile=row["mobile"],
            email=None,

            location_id=row["locations_id"],
            entity_id=row["entities_id"],
            group_id=row["groups_id"],

            is_active=bool(row["is_active"])
        )

    def find_by_id(self, user_id: int):

        sql = """
        SELECT
            u.id,
            u.name,
            u.firstname,
            u.realname,
            u.registration_number,
            u.phone,
            u.mobile,
            u.locations_id,
            u.entities_id,
            u.groups_id,
            u.is_active

        FROM glpi_users u

        WHERE u.id=%s
          AND u.is_deleted=0

        LIMIT 1
        """

        return self._row_to_requester(
            self.fetch_one(sql, (user_id,))
        )

    def find_by_mobile(self, mobile: str):

        sql = """
        SELECT
            u.id,
            u.name,
            u.firstname,
            u.realname,
            u.registration_number,
            u.phone,
            u.mobile,
            u.locations_id,
            u.entities_id,
            u.groups_id,
            u.is_active

        FROM glpi_users u

        WHERE u.mobile=%s
          AND u.is_deleted=0
          AND u.is_active=1

        LIMIT 1
        """

        return self._row_to_requester(
            self.fetch_one(sql, (mobile,))
        )

    def find_by_phone(self, phone: str):

        sql = """
        SELECT
            u.id,
            u.name,
            u.firstname,
            u.realname,
            u.registration_number,
            u.phone,
            u.mobile,
            u.locations_id,
            u.entities_id,
            u.groups_id,
            u.is_active

        FROM glpi_users u

        WHERE
            (
                u.phone=%s
                OR u.phone2=%s
                OR u.mobile=%s
            )
            AND u.is_deleted=0
            AND u.is_active=1

        LIMIT 1
        """

        return self._row_to_requester(
            self.fetch_one(
                sql,
                (
                    phone,
                    phone,
                    phone
                )
            )
        )

    def find_by_registration(self, registration):

        sql = """
        SELECT
            u.id,
            u.name,
            u.firstname,
            u.realname,
            u.registration_number,
            u.phone,
            u.mobile,
            u.locations_id,
            u.entities_id,
            u.groups_id,
            u.is_active

        FROM glpi_users u

        WHERE u.registration_number=%s
          AND u.is_deleted=0

        LIMIT 1
        """

        return self._row_to_requester(
            self.fetch_one(sql, (registration,))
        )

    def search_by_name(self, text):

        sql = """
        SELECT
            u.id,
            u.name,
            u.firstname,
            u.realname,
            u.registration_number,
            u.phone,
            u.mobile,
            u.locations_id,
            u.entities_id,
            u.groups_id,
            u.is_active

        FROM glpi_users u

        WHERE
            u.is_deleted=0
            AND (
                LOWER(
                    CONCAT_WS(
                        ' ',
                        u.firstname,
                        u.realname,
                        u.name
                    )
                )
                LIKE LOWER(%s)
            )

        ORDER BY
            u.firstname,
            u.realname

        LIMIT 10
        """

        like = f"%{text}%"

        return [
            self._row_to_requester(row)
            for row in self.fetch_all(sql, (like,))
        ]

    def search(self, value):

        value = normalize(value)

        if not value:
            return []

        if value.isdigit():

            user = self.find_by_registration(value)

            return [user] if user else []

        return self.search_by_name(value)
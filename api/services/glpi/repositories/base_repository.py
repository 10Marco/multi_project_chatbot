class BaseRepository:
    def __init__(self, connection):
        self.connection = connection

    def connect(self):
        return self.connection()

    def fetch_one(self, sql, params=()):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()

    def fetch_all(self, sql, params=()):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()

    def execute(self, sql, params=()):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.rowcount

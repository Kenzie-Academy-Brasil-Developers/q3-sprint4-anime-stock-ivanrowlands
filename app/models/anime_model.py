from app.models import DatabaseConnector
from psycopg2 import sql

class Anime(DatabaseConnector):
    anime_keys = ['id', 'anime', 'released_date', 'seasons']

    def __init__(self, *args, **kwargs) -> None:
        self.anime = kwargs['anime'].title()
        self.released_date = kwargs['released_date']
        self.seasons = kwargs['seasons']
    
    @classmethod
    def create_table(cls):
        cls.get_conn_cur()
        
        cls.cur.execute(""" 
            CREATE TABLE IF NOT EXISTS animes (
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            )
        """)

        cls.commit_and_close()

    @classmethod
    def get_all_animes(cls):
        cls.get_conn_cur()

        cls.cur.execute("SELECT * FROM animes")

        animes = cls.cur.fetchall()

        cls.commit_and_close()

        return animes

    @classmethod
    def get_anime_by_id(cls, anime_id: int):
        cls.get_conn_cur()

        query = "SELECT * FROM animes WHERE id = %s"

        cls.cur.execute(query,(anime_id,))

        anime = cls.cur.fetchone()

        cls.commit_and_close()

        return anime
    
    @classmethod
    def delete_anime(cls, anime_id: int):
        cls.get_conn_cur()

        query = "DELETE FROM animes WHERE id = %s"

        cls.cur.execute(query,(anime_id,))

        cls.commit_and_close()

    @classmethod
    def update_anime(cls, anime_id, payload):
        cls.get_conn_cur()

        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = ROW({values})
                WHERE
                    id={id}
                RETURNING *
            """
        ).format(
            id=sql.Literal(anime_id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cls.cur.execute(query)

        updated_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_anime
    
    @staticmethod
    def serialize_data(data, keys=anime_keys):
        if type(data) is tuple:
            return dict(zip(keys, data))
        if type(data) is list:
            return [dict(zip(keys, anime)) for anime in data]
    
    def create_anime(self):
        self.get_conn_cur()

        query = """
            INSERT INTO
                animes (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """

        query_values = list(self.__dict__.values())

        self.cur.execute(query, query_values)

        inserted_anime = self.cur.fetchone()

        self.commit_and_close()

        return inserted_anime
from platform import release
from syslog import closelog
from itsdangerous import Serializer
from app.models import DatabaseConnector
from flask import request

class Animes(DatabaseConnector):
    def __init__(self, *args, **kwargs):
        self.anime = kwargs['anime']
        self.released_date = kwargs['released_date']
        self.seasons = kwargs['seasons']

    def create_anime(self):
        self.get_conn_cur()  

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS animes(
            id BIGSERIAL PRIMARY KEY,
            anime VARCHAR(100) NOT NULL UNIQUE,
            released_date DATE NOT NULL,
            seasons INTEGER NOT NULL
            );
        """)

        self.conn.commit()
        self.cur_conn_close()

        self.get_conn_cur()

        query = """
            INSERT INTO
                animes (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """ 
        data = request.get_json()
        new_data = {}

        for key, value in data.items():
            if key == 'anime':
                new_data[key] = value.title()
            else:
                new_data[key] = value

        query_values = (new_data['anime'], new_data['released_date'], new_data['seasons'])

        self.cur.execute(query, query_values)
        self.conn.commit()
        self.cur_conn_close()

        self.get_conn_cur()

        data = ('DD/MM/YYYY', new_data['anime'])
        select = 'SELECT id, anime, to_char(released_date, (%s)) as released_date, seasons FROM animes WHERE anime = (%s)'

        self.cur.execute(select, data)

        getting_data = self.cur.fetchall()

        return getting_data
    
    @classmethod
    def read_animes(cls):
        cls.get_conn_cur()  

        cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS animes(
            id BIGSERIAL PRIMARY KEY,
            anime VARCHAR(100) NOT NULL UNIQUE,
            released_date DATE NOT NULL,
            seasons INTEGER NOT NULL
            );
        """)

        cls.conn.commit()
        cls.cur_conn_close()

        cls.get_conn_cur()

        data = ('DD/MM/YYYY',)
        select = 'SELECT id, anime, to_char(released_date, (%s)) as released_date, seasons FROM animes'

        cls.cur.execute(select, data)

        animes = cls.cur.fetchall()

        cls.cur_conn_close()

        return animes

    @classmethod
    def read_anime(cls, anime_id):
        cls.get_conn_cur()

        data = ('DD/MM/YYYY', anime_id)

        select = 'SELECT id, anime, to_char(released_date, (%s)) as released_date, seasons FROM animes WHERE id = (%s)'

        cls.cur.execute(select, data)

        getting_data = cls.cur.fetchall()

        return getting_data

    @classmethod
    def update_anime(cls, anime_id):
        cls.get_conn_cur()

        data = request.get_json()

        for key, value in data.items():
            change = (value, anime_id)
            if key == 'anime':
                new_value= value.title()
                change = (new_value, anime_id)
                update = 'UPDATE animes SET anime = %s WHERE id = %s'
                cls.cur.execute(update, change)
            elif key == 'released_date':
                update = 'UPDATE animes SET released_date = %s WHERE id = %s'
                cls.cur.execute(update, change)
            elif key == 'seasons':
                update = 'UPDATE animes SET seasons = %s WHERE id = %s'
                cls.cur.execute(update, change)
            else:
                return key
            cls.conn.commit()
        
        cls.cur_conn_close()

        cls.get_conn_cur()
        query = ('DD/MM/YYYY', anime_id)

        select = 'SELECT id, anime, to_char(released_date, (%s)) as released_date, seasons FROM animes WHERE id = (%s)'

        cls.cur.execute(select, query)

        getting_data = cls.cur.fetchall()

        return getting_data

    @classmethod
    def delete_anime(cls, anime_id):
        cls.get_conn_cur()

        query = (anime_id,)

        delete = 'DELETE FROM animes WHERE id = %s RETURNING *'

        cls.cur.execute(delete, query)

        getting_data = cls.cur.fetchall()

        if len(getting_data) == 0:
            return False

        cls.conn.commit()
        
        cls.cur_conn_close()

        return True
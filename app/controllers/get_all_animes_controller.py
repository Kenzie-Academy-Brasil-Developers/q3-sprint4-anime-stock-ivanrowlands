from flask import jsonify
from psycopg2.errors import UndefinedTable

from app.models.anime_model import Anime

def get_all():
    try:
        Anime.get_all_animes()
    except UndefinedTable:
        Anime.create_table()

    animes_list = Anime.get_all_animes()

    seriliazed_list = Anime.serialize_data(animes_list)

    return jsonify(data= seriliazed_list), 200
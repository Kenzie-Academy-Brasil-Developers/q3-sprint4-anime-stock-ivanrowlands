from flask import jsonify
from psycopg2.errors import UndefinedTable

from app.models.anime_model import Anime

def get_by_id(anime_id: int):
    try:
        Anime.get_anime_by_id(anime_id)
    except UndefinedTable:
        Anime.create_table()

    anime = Anime.get_anime_by_id(anime_id)
   
    serialized_anime = Anime.serialize_data(anime)
    
    if anime == None:
        return jsonify(erro= "Not Found"), 404

    return jsonify(data= serialized_anime), 200
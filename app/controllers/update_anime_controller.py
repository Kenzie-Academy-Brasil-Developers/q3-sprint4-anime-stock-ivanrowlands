from flask import jsonify, request
from psycopg2.errors import UndefinedTable, UndefinedColumn

from app.models.anime_model import Anime

def update_anime(anime_id: int):
    data = request.get_json()

    try:
        Anime.get_anime_by_id(anime_id)
    except UndefinedTable:
        Anime.create_table()
    
    anime = Anime.get_anime_by_id(anime_id)
   
    if anime == None:
        return jsonify(erro= "Not Found"), 404

    try:
        Anime.update_anime(anime_id, data)
    except UndefinedColumn:
        return {
                    "available_keys": [
                    "anime",
                    "seasons",
                    "released_date"
                    ],
                    "received": list(data.keys())
                 }, 422
    
    updated_anime = Anime.update_anime(anime_id, data)

    serialize_anime = Anime.serialize_data(updated_anime)

    return jsonify(serialize_anime), 200
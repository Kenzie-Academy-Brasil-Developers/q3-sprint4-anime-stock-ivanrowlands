from flask import jsonify, request
from psycopg2.errors import UndefinedTable, UniqueViolation

from app.models.anime_model import Anime

def create():
    data = request.get_json()

    try:
        anime = Anime(**data)
    except KeyError:
         return {
                    "available_keys": [
                    "anime",
                    "seasons",
                    "released_date"
                    ],
                    "received": list(data.keys())
                 }, 422
    try:
        new_anime = anime.create_anime()
    except UndefinedTable:
        Anime.create_table()
    except UniqueViolation:
        return {"error": "anime already exists"}, 409

    serialized_anime = Anime.serialize_data(new_anime)

    return jsonify(serialized_anime), 201
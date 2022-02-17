from flask import jsonify, request
from app.models.animes_model import Animes
from psycopg2.errors import UniqueViolation, UndefinedTable


def get_animes():
   animes = Animes.read_animes()

   animes_keys = ['id', 'anime', 'released_date', 'seasons']

   animes_list = [dict(zip(animes_keys, anime)) for anime in animes]

   return {"data": animes_list}, 200

def create_anime():
   try: 
      data = request.get_json()

      anime = Animes(**data)

      inserted_user = anime.create_anime()

      animes_keys = ['id', 'anime', 'released_date', 'seasons']

      inserted_user = dict(zip(animes_keys, inserted_user[0]))


      return jsonify(inserted_user), 201
   
   except KeyError:
      data = request.get_json()
      for key in data.keys():
         if key != 'anime' and key != 'released_date' and key != 'seasons':
            wrong_key = key
      return {"available_keys": ["anime", "released_date", "seasons"], "wrong_keys_sended":[wrong_key]}, 422
   
   except UniqueViolation:
      return {"error": "anime is already exists"}, 422

def get_anime(anime_id):
   try:
      anime = Animes.read_anime(anime_id)

      if len(anime) == 0:
         return {"error": "Not Found"}, 404

      anime_keys = ['id', 'anime', 'released_date', 'seasons']

      anime_list = [dict(zip(anime_keys, anime[0])) for a in anime]

      return {"data": anime_list}, 200
   except UndefinedTable:
      return {"error": "Not Found"}, 404

def update_anime(anime_id):
   try:
      anime = Animes.update_anime(anime_id)

      if type(anime) == str:
         return {"available_keys": ["anime", "released_date", "seasons"], "wrong_keys_sended":[anime]}, 422

      if len(anime) == 0:
         return {"error": "Not Found"}, 404

      anime_keys = ['id', 'anime', 'released_date', 'seasons']

      anime_list = [dict(zip(anime_keys, anime[0])) for a in anime]

      return {"data": anime_list}, 200
   except UndefinedTable:
      return {"error": "Not Found"}, 404

def delete_anime(anime_id):
   try:
      anime = Animes.delete_anime(anime_id)

      if anime == True:
         return "", 204
      return {"error": "Not Found"}, 404
   except UndefinedTable:
      return {"error": "Not Found"}, 404
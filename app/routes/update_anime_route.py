from flask import Blueprint

from app.controllers.update_anime_controller import update_anime
bp_update_anime = Blueprint("update_anime", __name__)

bp_update_anime.patch('/animes/<int:anime_id>')(update_anime)
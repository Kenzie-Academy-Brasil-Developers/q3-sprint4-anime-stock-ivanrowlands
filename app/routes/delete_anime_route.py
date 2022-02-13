from flask import Blueprint

from app.controllers.delete_anime_controller import delete
bp_animes = Blueprint("delete_anime", __name__)

bp_animes.delete('/animes/<int:anime_id>')(delete)
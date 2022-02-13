from flask import Blueprint

from app.controllers.get_anime_by_id_controller import get_by_id
bp_get_anime_by_id = Blueprint("get_anime_by_id", __name__)

bp_get_anime_by_id.get('/animes/<int:anime_id>')(get_by_id)
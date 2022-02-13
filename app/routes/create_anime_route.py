from flask import Blueprint

from app.controllers.create_anime_controller import create
bp_create_anime = Blueprint("create_anime", __name__)

bp_create_anime.post('/animes')(create)
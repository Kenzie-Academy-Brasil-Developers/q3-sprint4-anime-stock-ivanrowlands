from flask import Flask, Blueprint
from app.controllers import animes_controller

bp = Blueprint("animes", __name__, url_prefix='/animes')

@bp.get('')
def retrieve():
    return animes_controller.get_animes()

@bp.post('')
def post_anime():
    return animes_controller.create_anime()

@bp.get('/<int:anime_id>')
def get_anime(anime_id):
    return animes_controller.get_anime(anime_id)

@bp.patch('/<int:anime_id>')
def patch_anime(anime_id):
    return animes_controller.update_anime(anime_id)

@bp.delete('/<int:anime_id>')
def delete_anime(anime_id):
    return animes_controller.delete_anime(anime_id)
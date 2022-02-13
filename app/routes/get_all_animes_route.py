import imp
from flask import Blueprint

from app.controllers.get_all_animes_controller import get_all
bp_get_all_animes = Blueprint("get_all_animes", __name__)

bp_get_all_animes.get('/animes')(get_all)
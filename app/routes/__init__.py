from flask import Flask

from app.routes.create_anime_route    import bp_create_anime
from app.routes.delete_anime_route    import bp_animes
from app.routes.get_all_animes_route  import bp_get_all_animes
from app.routes.get_anime_by_id_route import bp_get_anime_by_id
from app.routes.update_anime_route    import bp_update_anime

def init_app(app: Flask):
    app.register_blueprint(bp_update_anime)
    app.register_blueprint(bp_animes)
    app.register_blueprint(bp_create_anime)
    app.register_blueprint(bp_get_all_animes)
    app.register_blueprint(bp_get_anime_by_id)
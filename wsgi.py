import bottle

from db import bottle_sqlalchemy
from db.engine import engine
from views.admin import save_post, posts_list, logout, edit_post, new_post, init_db, main_admin, delete_post
from views.posts import main, view_post
from views.search import search
from views.static import stylesheets, jscripts, images

app = bottle.Bottle()
db_plugin = bottle_sqlalchemy.Plugin(
    engine,
    keyword='db',
    use_kwargs=False
)
app.install(db_plugin)
bottle.TEMPLATE_PATH = ["templates/"]


def setup_routing(bottle_app):
    # static
    bottle_app.route("/css/<filename:re:.*\.css>", ["GET"], stylesheets)
    bottle_app.route("/js/<filename:re:.*\.js>", ["GET"], jscripts)
    bottle_app.route("/img/<filename:re:.*\.(png|jpg)>", ["GET"], images)

    # posts
    bottle_app.route("/", ["GET"], main)
    bottle_app.route("/read/<post_id>/", ["GET"], view_post)
    bottle_app.route("/search/", ["GET"], search)

    # admin
    bottle_app.route("/master/", ["GET"], main_admin)
    bottle_app.route("/master/save-post/", ["POST"], save_post)
    bottle_app.route("/master/posts/", ["GET"], posts_list)
    bottle_app.route("/master/post/delete/<post_id>/", ["GET"], delete_post)
    bottle_app.route("/master/post/<post_id>/", ["GET"], edit_post)
    bottle_app.route("/master/post/", ["GET"], new_post)
    bottle_app.route("/master/init-db/", ["GET"], init_db)
    bottle_app.route("/master/logout/", ["GET"], logout)


@app.error(401)
def error_401(error):
    return bottle.template("errors/401")


setup_routing(app)
bottle.debug(True)

if __name__ == "__main__":
    bottle.run(app, host="0.0.0.0", port=8003, reloader=True)



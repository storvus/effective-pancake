import bottle

from models.base import Base
from models.post import Post
from utils.lib import update_post_by_id, create_post, yes_master
from utils.paginator import Paginator


@bottle.auth_basic(yes_master)
def main_admin():
    return bottle.template("admin/main", {"base": "Main page", "title": "Main"})


def logout():
    return bottle.abort(401)


@bottle.auth_basic(yes_master)
def new_post():
    return bottle.template("admin/edit_post", {"post": None})


@bottle.auth_basic(yes_master)
def edit_post(db, post_id):
    post = db.query(Post).get(post_id)
    return bottle.template(
        "admin/edit_post",
        {
            "post": post
        }
    )


@bottle.auth_basic(yes_master)
def save_post(db):
    post_id = bottle.request.forms.get("post_id")
    if post_id:
        post = db.query(Post).get(post_id)
    else:
        post = Post()
    post.name = bottle.request.forms["name"]
    post.body = bottle.request.forms["body"]
    db.commit()
    # ToDo: add flash messages - bottle_utils.flash + bootstrap toast
    return bottle.redirect(f"/master/post/{post.id}/")


@bottle.auth_basic(yes_master)
def delete_post(db, post_id):
    db.query(Post).filter(Post.id == post_id).delete()
    # ToDo: add flash messages - bottle_utils.flash + bootstrap toast
    return bottle.redirect(f"/master/posts/")


@bottle.auth_basic(yes_master)
def posts_list(db):
    posts = db.query(Post).order_by(Post.id.desc())
    paginator = Paginator(records_count=posts.count())

    return bottle.template(
        "admin/posts",
        {
            "paginator": paginator.render(),
            "posts": posts.all(),
        }
    )


@bottle.auth_basic(yes_master)
def init_db(db):
    Base.metadata.create_all(db.bind)
    return bottle.template("admin/main", {"base": "OK", "title": "DB init"})

import bottle

from utils.lib import update_post_by_id, create_post, get_posts_list, yes_master, get_post_by_id


@bottle.auth_basic(yes_master)
def main_admin():
    return bottle.template("admin/main", {"body": ""})


def logout():
    return bottle.abort(401)


@bottle.auth_basic(yes_master)
def new_post():
    return bottle.template("admin/edit_post", {"post": None})


@bottle.auth_basic(yes_master)
def edit_post(db, post_id):
    post = get_post_by_id(db, post_id)
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
        update_post_by_id(db, post_id, bottle.request.forms["name"], bottle.request.forms["body"])
    else:
        post_id = create_post(db, bottle.request.forms["name"], bottle.request.forms["body"])
    # ToDo: add flash messages - bottle_utils.flash + bootstrap toast
    return bottle.redirect(f"/master/post/{post_id}/")


@bottle.auth_basic(yes_master)
def posts_list(db):
    posts = bottle.template(
        "admin/posts",
        {
            "posts": get_posts_list(db, page=1, per_page=100)
        }
    )
    return bottle.template("admin/main", {"body": posts})


@bottle.auth_basic(yes_master)
def init_db(db):
    c = db.cursor()
    # c.execute(
    #     """
    #         CREATE TABLE IF NOT EXISTS tags (
    #             id integer PRIMARY KEY,
    #             name text NOT NULL
    #         );
    #     """
    # )
    c.execute(
        """
            CREATE TABLE IF NOT EXISTS posts (
                id integer PRIMARY KEY,
                body text NOT NULL,
                name text NOT NULL,
                publish_date INTEGER NOT NULL
            );
        """
    )
    # c.execute(
    #     """
    #         CREATE TABLE IF NOT EXISTS tags_posts (
    #             tag_id integer NOT NULL,
    #             post_id integer NOT NULL,
    #             FOREIGN KEY(tag_id) REFERENCES tags(id),
    #             FOREIGN KEY(post_id) REFERENCES posts(id)
    #         );
    #     """
    # )
    c.close()
    return bottle.template("admin/main", {"body": "OK"})

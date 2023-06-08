from datetime import datetime

import bottle
import markdown2

from models.post import Post
from utils.paginator import Paginator


# ToDo: add users' comments to posts

def main(db):
    posts = db.query(Post).order_by(Post.id.desc())
    paginator = Paginator(records_count=posts.count())
    posts.limit(paginator.limit).offset(paginator.offset)
    return bottle.template(
        "posts",
        {
            "paginator": paginator.render(),
            "posts": posts
        }
    )


def view_post(db, post_id):
    post = db.query(Post).get(post_id)
    return bottle.template(
        "post",
        {
            "post": post
        }
    )

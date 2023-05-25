import math
from datetime import datetime

import bottle
import markdown

from config import POSTS_PER_PAGE
from utils.lib import get_posts_list, get_pagination_page, get_posts_count


def main(db):
    page = get_pagination_page()
    posts_count = get_posts_count(db)
    pages_count = math.ceil(posts_count / POSTS_PER_PAGE)
    if page > pages_count:
        page = 1

    posts = get_posts_list(db, page)

    posts_template = bottle.template(
        "posts",
        {
            "page": page,
            "pages_count": pages_count,
            "posts": [{
                **post,
                "body": markdown.markdown(post["body"], extensions=["codehilite"]),
                "publish_date": datetime.fromtimestamp(post["publish_date"]).strftime("%Y-%m-%d %H:%M"),
            } for post in posts]
        }
    )
    return bottle.template("base", {"body": posts_template})

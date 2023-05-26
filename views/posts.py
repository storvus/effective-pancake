from datetime import datetime

import bottle
import markdown

from utils.lib import get_posts_list, get_posts_count
from utils.paginator import Paginator


def main(db):
    posts_count = get_posts_count(db)
    paginator = Paginator(records_count=posts_count)
    posts = get_posts_list(db, paginator)

    posts_template = bottle.template(
        "posts",
        {
            "paginator": paginator.render(),
            "posts": [{
                **post,
                "body": markdown.markdown(post["body"], extensions=["codehilite"]),
                "publish_date": datetime.fromtimestamp(post["publish_date"]).strftime("%Y-%m-%d %H:%M"),
            } for post in posts]
        }
    )
    return bottle.template("base", {"body": posts_template})

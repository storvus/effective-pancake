from datetime import datetime

import bottle
import markdown2

from utils.lib import get_posts_list, get_posts_count, get_post_by_id
from utils.paginator import Paginator


# ToDo: add users' comments to posts

def main(db):
    posts_count = get_posts_count(db)
    paginator = Paginator(records_count=posts_count)
    posts = get_posts_list(db, paginator)

    return bottle.template(
        "posts",
        {
            "paginator": paginator.render(),
            "search_term": "",
            "posts": [{
                **post,
                "body": markdown2.markdown(post["body"], extras=["nofollow", "task_list", "fenced-code-blocks", "pyshell"]),
                "publish_date": datetime.fromtimestamp(post["publish_date"]).strftime("%Y-%m-%d %H:%M"),
            } for post in posts]
        }
    )


def view_post(db, post_id):
    post = get_post_by_id(db, post_id)
    return bottle.template(
        "post",
        {
            "search_term": "",
            "post": {
                **post,
                "body": markdown2.markdown(post["body"], extras=["nofollow", "task_list", "fenced-code-blocks", "pyshell"]),
                "publish_date": datetime.fromtimestamp(post["publish_date"]).strftime("%Y-%m-%d %H:%M"),
            }
        }
    )

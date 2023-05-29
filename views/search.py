from datetime import datetime

import bottle
import markdown2

from utils.lib import search_posts


def search(db):
    search_term = bottle.request.GET.get("search")
    if not search_term:
        return bottle.redirect("/")
    posts = search_posts(db, search_term)
    if not posts:
        search = bottle.template("search")
        return bottle.template("base", {"body": search, "search_term": search_term})
    posts_template = bottle.template(
        "posts",
        {
            "paginator": "",
            "posts": [{
                **post,
                "body": markdown2.markdown(post["body"], extras=["nofollow", "task_list", "fenced-code-blocks"]),
                "publish_date": datetime.fromtimestamp(post["publish_date"]).strftime("%Y-%m-%d %H:%M"),
            } for post in posts]
        }
    )
    return bottle.template("base", {"body": posts_template, "search_term": search_term})

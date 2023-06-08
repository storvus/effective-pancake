import bottle
from sqlalchemy import or_

from models.post import Post


def search(db):
    search_term = bottle.request.GET.get("search")
    if not search_term:
        return bottle.redirect("/")
    posts = db.query(Post).filter(or_(
        Post.name.ilike(f"%{search_term}%"),
        Post.body.ilike(f"%{search_term}%"),
    )).order_by(Post.id.desc())

    if not posts.count():
        return bottle.template("search", {"search_term": search_term})

    return bottle.template(
        "posts",
        {
            "paginator": "",
            "search_term": search_term,
            "posts": posts,
        }
    )

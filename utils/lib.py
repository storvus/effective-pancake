import time
from typing import List

from utils.paginator import BasePaginator
from utils.typing import Post


def yes_master(user, password):
    return user == password


def get_posts_list(db, paginator: BasePaginator) -> List[Post]:
    cur = db.cursor()
    cur.execute("SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?", (paginator.limit, paginator.offset))
    return cur.fetchall()


def get_post_by_id(db, post_id) -> Post:
    post_id = int(post_id)
    cur = db.cursor()
    cur.execute("SELECT * FROM posts WHERE id = ?", (post_id, ))
    return cur.fetchone()


def update_post_by_id(db, post_id, name, body):
    post_id = int(post_id)
    cur = db.cursor()
    cur.execute("UPDATE posts SET name = ?, body = ? WHERE id = ?", (name, body, post_id))


def create_post(db, name, body) -> int:
    cur = db.cursor()
    cur.execute("INSERT INTO posts (body, name, publish_date) VALUES (?, ?, ?)", (body, name, time.time()))
    return cur.lastrowid


def get_posts_count(db):
    cur = db.cursor()
    cur.execute("SELECT count(*) as count FROM posts")
    return cur.fetchone()["count"]

import time
from typing import List

from models.post import Post
from utils.paginator import BasePaginator


def yes_master(user, password):
    return user == password


def search_posts(db, search_term: str) -> List[Post]:
    search_term = f"%{search_term}%"
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM posts WHERE body LIKE ? OR name LIKE ? ORDER BY id DESC",
        (search_term, search_term, )
    )
    return cur.fetchall()


def update_post_by_id(db, post_id, name, body):
    post_id = int(post_id)
    cur = db.cursor()
    cur.execute("UPDATE posts SET name = ?, body = ? WHERE id = ?", (name, body, post_id))


def create_post(db, name, body) -> int:
    cur = db.cursor()
    cur.execute("INSERT INTO posts (body, name, publish_date) VALUES (?, ?, ?)", (body, name, time.time()))
    return cur.lastrowid


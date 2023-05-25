from typing_extensions import TypedDict


class Post(TypedDict):
    id: int
    name: str
    body: str
    publish_date: int

from datetime import datetime
from typing import List

import markdown2
from sqlalchemy import Text, String, Integer, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

posts_tags = Table(
    "posts_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(255))
    publish_date: Mapped[int] = mapped_column(Integer)
    tags: Mapped[List["Tag"]] = relationship(secondary=posts_tags, back_populates="posts")

    def __repr__(self) -> str:
        return self.name

    @property
    def formatted_body(self):
        return markdown2.markdown(self.body, extras=["nofollow", "task_list", "fenced-code-blocks", "pyshell"])

    @property
    def formatted_publish_date(self):
        return datetime.fromtimestamp(self.publish_date).strftime("%Y-%m-%d %H:%M")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    posts: Mapped[List[Post]] = relationship(secondary=posts_tags, back_populates="tags")

    def __repr__(self) -> str:
        return self.name



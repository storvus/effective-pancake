import math

import bottle

from config import POSTS_PER_PAGE


class BasePaginator:

    @property
    def limit(self):
        raise NotImplementedError

    @property
    def offset(self):
        raise NotImplementedError


class Paginator(BasePaginator):

    def __init__(self, records_count: int, per_page: int = POSTS_PER_PAGE) -> None:
        self.per_page = per_page
        self.pages_count = math.ceil(records_count / per_page)
        self.page = self._get_pagination_page()
        if self.pages_count < self.page:
            self.page = self.pages_count

    def render(self) -> str:
        return bottle.template("common/paginator", {"page": self.page, "pages_count": self.pages_count})

    @staticmethod
    def _get_pagination_page() -> int:
        try:
            return int(bottle.request.GET.get("page", 1))
        except TypeError:
            return 1

    @property
    def limit(self) -> int:
        return self.per_page

    @property
    def offset(self) -> int:
        return self.per_page * (self.page - 1)

import math

import bottle


class Paginator:

    def __init__(self, page: int, per_page: int, records_count: int) -> None:
        self.page = page
        self.per_page = per_page
        self.pages_count = math.ceil(records_count / per_page)

    def render(self):
        return bottle.template("common/paginator", {"page": self.page, "pages_count": self.pages_count})

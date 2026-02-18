from pydantic import BaseModel


class LinksRegister(BaseModel):
    links: dict[str, list[tuple[int, float, float, float, float]]] = {}
    """id, list[tuple[page_number, x, y, w, h]]"""
    link_targets: dict[str, tuple[int, float, float]] = {}
    """id, tuple[page_number, x, y]"""
    page_sizes: dict[int, tuple[float, float]] = {}
    """page_number, tuple[w, h]"""

    def register_link(self, link_target: str, page_number: int, x: float, y: float, width: float, height: float):
        if not link_target in self.links.keys():
            self.links[link_target] = []

        self.links[link_target].append((page_number, x, y, width, height))

    def register_link_target(self, link_target: str, page_number: int, x: float, y: float):
        self.link_targets[link_target] = (page_number, x, y)

    def register_page(self, page_number: int, width: float, height: float):
        self.page_sizes[page_number] = (width, height)

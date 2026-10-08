from pydantic import BaseModel

from svk.data._label import Label


class Translator(BaseModel):
    lang: str = "nl"
    """supported values: nl (for Dutch) and en (for English)"""

    def get_label(self, label: Label) -> str:
        return label.en if self.lang == "en" else label.nl

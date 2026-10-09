from pydantic import BaseModel, ConfigDict

from svk.data._label import Label


class Translator(BaseModel):
    model_config = ConfigDict(frozen=True)

    lang: str = "nl"  # COnsider using an enum value instead of strings. It can only be 2 values.
    """supported values: nl (for Dutch) and en (for English)"""

    def get_label(self, label: Label) -> str:
        return label.en if self.lang == "en" else label.nl

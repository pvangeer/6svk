from enum import Enum
from pathlib import Path


class BarrierIcons(Enum):
    __icon_base_path = Path(__file__).resolve().parent
    MaeslantBarrier = str(__icon_base_path / "MaeslantKering.svg")
    HartelBarrier = str(__icon_base_path / "MaeslantKering.svg")

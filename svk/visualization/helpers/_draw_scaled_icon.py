from svgwrite import Drawing
from svk.visualization.helpers.icons._icons import BarrierIcons
from uuid import uuid4
from pydantic import BaseModel
from abc import ABC, abstractmethod

accent_fill = "#a7a7a7"


class SvgObject(ABC, BaseModel):
    @abstractmethod
    def create(self, dwg: Drawing):
        pass


class Symbol(SvgObject):
    width: float = 300
    height: float = 300
    objects: list[SvgObject] = []

    def create(self, dwg: Drawing):
        icon_symbol = dwg.symbol(id=f"icon_{ uuid4()}", viewBox=f"0 0 {self.width} {self.height}")
        for svg_object in self.objects:
            icon_symbol.add(svg_object.create(dwg))

        return icon_symbol

    def add_to_dwg(self, dwg: Drawing, insert: tuple[float, float], size: tuple[float, float]) -> None:
        icon_symbol = self.create(dwg)
        dwg.defs.add(icon_symbol)
        dwg.add(dwg.use(icon_symbol, insert=insert, size=size))


class Path(SvgObject):
    d: str
    fill: str = "none"
    transform: str | None = None
    stroke_linecap: str = "round"
    stroke_linejoin: str = "round"
    stroke_width: float = 20.0

    def create(self, dwg: Drawing):
        if self.transform is None:
            return dwg.path(
                d=self.d,
                fill=self.fill,
                stroke="black",
                stroke_linecap=self.stroke_linecap,
                stroke_linejoin=self.stroke_linejoin,
                stroke_width=self.stroke_width,
            )
        else:
            return dwg.path(
                d=self.d,
                fill=self.fill,
                stroke="black",
                stroke_linecap=self.stroke_linecap,
                stroke_linejoin=self.stroke_linejoin,
                stroke_width=self.stroke_width,
                transform=self.transform,
            )


class Rect(SvgObject):
    x: float
    y: float
    width: float
    height: float
    stroke: str = "#000000"
    stroke_width: float = 20
    strok_linejoin: str = "round"
    stroke_linecap: str = "round"
    fill: str = "#000000"

    def create(self, dwg: Drawing) -> None:
        return dwg.rect(
            insert=(self.x, self.y),
            size=(self.width, self.height),
            fill=self.fill,
            stroke=self.stroke,
            stroke_width=self.stroke_width,
            stroke_linecap=self.stroke_linecap,
            stroke_linejoin=self.strok_linejoin,
        )


def draw_scaled_icon(dwg: Drawing, icon: BarrierIcons, insert: tuple[float, float], size: tuple[float, float] = (24, 24)):
    ico = Symbol()
    match icon:
        case BarrierIcons.MaeslantBarrier:
            ico.objects = [
                Path(d="M 24.170359,196.3714 C 68.915299,121.29763 153.13367,157.57441 153.13367,157.57441"),
                Path(d="M 170.32004,147.49117 C 166.56264,51.164433 240.06307,35.859115 240.06307,35.859115"),
                Path(
                    d="m 46.695954,175.10982 59.056636,84.46477 15.10753,-104.03585 m 59.00465,-36.61713 100.94565,19.22777 -61.80346,-86.181516 m 13.76036,77.088746 -13.39074,-76.567648 m 32.22464,46.150649 -72.10403,19.914429",
                    stroke_width=10,
                ),
                Path(d="M 112.0344,218.59687 48.514185,177.73789 m 32.984057,45.65986 39.485568,-66.61042", stroke_width=10),
            ]
        case BarrierIcons.HaringvlietBarrier:
            ico.objects = [
                Path(d="M 51.638567,218.00261 C 18.139966,185.89907 19.91285,142.81025 19.91285,142.81025"),
                Path(d="m 283.62638,163.97208 c -6.25032,42.98142 -16.43842,55.23733 -16.43842,55.23733"),
                Path(
                    d="m 49.442776,208.75838 76.910984,-71.41731 -98.885556,17.16761 m 251.625456,16.60254 -113.30637,-31.24507 101.63238,75.1942 M 207.69651,110.29944 84.432913,109.95609 M 274.89266,233.67007 37.635997,232.98337",
                    stroke_width=10,
                ),
                Path(
                    d="m 45.322541,84.464738 -29.249338,-50.06664 -29.24934,-50.066643 57.983651,-0.29735 57.983656,-0.29735 -28.734314,50.36399 z",
                    stroke_width=10,
                    fill=accent_fill,
                    transform="matrix(0.75456845,0,0,0.56407441,110.91278,121.99129)",
                ),
            ]
        case BarrierIcons.HartelBarrier:
            ico.objects = [
                Path(
                    d="M 32.719705,119.49805 C 142.37679,26.445768 215.95329,38.323024 259.62374,39.121386 v 88.200944 c -68.85629,51.38753 -147.47737,63.81212 -228.32663,69.7072 z",
                    stroke_width=10,
                    fill=accent_fill,
                ),
                Path(d="M 30.154808,260.33504 V 119.49805"),
                Path(d="M 258.25088,182.1445 V 41.307507"),
                Path(
                    d="m 32.008407,123.76584 c 0,0 75.339703,-3.11429 131.590113,-22.05024 77.1771,-25.980644 93.89133,-57.615128 93.89133,-57.615128"
                ),
                Path(
                    d="m 30.585812,118.78675 c 0,0 37.239771,-41.162762 108.828578,-62.594213 70.33467,-21.056 117.36416,-15.648555 117.36416,-15.648555"
                ),
                Path(
                    d="m 30.588689,194.58625 c 0,0 75.695341,-2.75864 131.945751,-21.69459 77.1771,-25.98065 95.47911,-47.86534 95.47911,-47.86534"
                ),
            ]
        case BarrierIcons.Ramspol:
            ico.objects = [
                Path(d="m 108.51657,222.68539 c -35.403564,-269.85873 267.57095,-92.02657 31.28754,-0.0425", fill=accent_fill),
                Path(d="M 8.2382951,105.06773 116.74205,104.72071", stroke_width=10),
                Path(d="m 226.25716,166.70787 64.74651,0.1839", stroke_width=10),
            ]
        case BarrierIcons.EasternScheldBarrier:
            ico.objects = [
                Rect(
                    x=66.862007,
                    y=180.31404,
                    width=168.57761,
                    height=51.213451,
                    fill=accent_fill,
                    stroke_width=10.0,
                ),
                Rect(
                    x=34.976582,
                    y=120.26601,
                    width=46.28627,
                    height=148.67361,
                    stroke_width=10.0,
                ),
                Rect(
                    x=220.18346,
                    y=120.26601,
                    width=46.28627,
                    height=148.67361,
                    stroke_width=10.0,
                ),
                Path(d="M 45.902124,121.32186 45.546474,56.949401", stroke_width=10.0),
                Path(d="M 71.974039,121.32186 71.618389,56.9494", stroke_width=10.0),
                Path(d="M 231.11045,121.32186 230.7548,56.949399", stroke_width=10.0),
                Path(d="M 257.52939,121.32186 257.17374,56.9494", stroke_width=10.0),
                Path(d="m 64.727389,161.1493 173.202481,-0.0806 v 0", fill=accent_fill),
            ]
        case BarrierIcons.HollandseIJsselBarrier:
            ico.objects = [
                Path(
                    d="M 44.405365,174.76525 196.62312,119.63966 196.97877,71.271404 42.982775,124.61875 Z",
                    stroke_width=10,
                    fill=accent_fill,
                ),
                Path(d="M 40.062225,216.37618 V 75.539194"),
                Path(d="M 196.3172,174.10619 V 33.269194"),
                Path(
                    d="m 101.35995,235.79526 152.21776,-55.12559 0.35565,-48.36826 -153.996003,53.34735 z",
                    stroke_width=10,
                    fill=accent_fill,
                ),
                Path(d="M 97.016813,277.40619 V 136.5692"),
                Path(d="M 253.27179,235.1362 V 94.299203"),
            ]
        case _:
            return

    ico.add_to_dwg(dwg=dwg, insert=insert, size=size)

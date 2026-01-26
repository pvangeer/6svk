from svgwrite import Drawing, etree
from svk.visualization.helpers.icons._icons import BarrierIcons
from uuid import uuid4
import xml.etree.ElementTree as et

from svgwrite import rgb


def parse_style(style):
    """
    Parse style string and return dict of valid svgwrite attributes.
    """
    style_dict = {}
    for item in style.split(";"):
        if ":" not in item:
            continue
        k, v = item.split(":")
        k = k.strip()
        v = v.strip()

        if v is None or v == "none":
            continue

        if k in {"stroke-width", "opacity", "fill-opacity", "stroke-opacity"}:
            try:
                style_dict[k] = float(v)
            except ValueError:
                continue  # ignore invalid numeric

        elif k == "stroke-dasharray":
            style_dict[k] = [float(x) for x in v.split(",")]

        else:
            style_dict[k] = v

    return style_dict


STYLE_ATTRS = [
    "fill",
    "fill-opacity",
    "stroke",
    "stroke-width",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke-dasharray",
    "stroke-dashoffset",
    "opacity",
    "transform",
]

INVALID_ATTRS = {
    "transform-center-x",
    "transform-center-y",
}


def split_attr(attr: str) -> tuple[str | None, str]:
    """
    Returns (namespace, localname)
    """
    if attr.startswith("{"):
        ns, local = attr[1:].split("}", 1)
        return ns, local
    return None, attr


def draw_scaled_icon(dwg: Drawing, icon: BarrierIcons, insert: tuple[float, float], size: tuple[float, float] = (24, 24)):
    path_coordinates = []
    stroke_linecap = "round"
    stroke_linejoin = "round"
    stroke_width = 20.0
    g_width = 300
    g_height = 300
    match icon:
        case BarrierIcons.MaeslantBarrier:
            # TODO: Adjust lines. Maybe add stroke_width to each line specific?
            path_coordinates = [
                "M 11.466313,219.37603 C 49.000848,134.00168 132.87586,139.72008 132.87586,139.72008",
                "M 143.32849,131.69695 C 138.54103,50.82108 211.69811,13.197843 211.69811,13.197843",
                "M 20.601156,204.9815 127.38381,262.66474 112.96301,142.83468",
                "m 147.98497,110.21618 121.54681,11.67399 -73.1341,-94.421962",
                "M 103.34913,151.41849 63.176877,225.58266 119.48671,215.28207",
                "m 145.92485,108.84277 c 26.3237,-13.734102 51.27399,-29.871673 76.22428,-45.665891 l 2.06011,51.159541",
            ]
        case BarrierIcons.MaeslantBarrier:
            path_coordinates = [
                "M 11.466313,219.37603 C 49.000848,134.00168 132.87586,139.72008 132.87586,139.72008",
                "M 143.32849,131.69695 C 138.54103,50.82108 211.69811,13.197843 211.69811,13.197843",
                "M 20.601156,204.9815 127.38381,262.66474 112.96301,142.83468",
                "m 147.98497,110.21618 121.54681,11.67399 -73.1341,-94.421962",
                "M 103.34913,151.41849 63.176877,225.58266 119.48671,215.28207",
                "m 145.92485,108.84277 c 26.3237,-13.734102 51.27399,-29.871673 76.22428,-45.665891 l 2.06011,51.159541",
            ]
        case _:
            return

    icon_symbol = dwg.symbol(id=f"icon_{ uuid4()}", viewBox=f"0 0 {g_width} {g_height}")
    for c in path_coordinates:
        icon_symbol.add(
            dwg.path(
                d=c, fill="none", stroke="black", stroke_linecap=stroke_linecap, stroke_linejoin=stroke_linejoin, stroke_width=stroke_width
            )
        )

    dwg.defs.add(icon_symbol)  # TODO: This needs to be done only once. We can refer to it from other locations.

    dwg.add(dwg.use(icon_symbol, insert=insert, size=size))


# def draw_scaled_icon(dwg: Drawing, icon_path: str, width: float, height: float):
#     tree = et.parse(icon_path)
#     root = tree.getroot()

#     ns = {"svg": "http://www.w3.org/2000/svg"}
#     group = dwg.g(transform="scale(0.5)")

#     for path_element in root.findall(".//svg:path", ns):
#         d = path_element.get("d")
#         if not d:
#             continue

#         new_path = dwg.path(d=d)

#         for k, v in path_element.attrib.items():
#             ns, k_local = split_attr(k)
#             if k in {"d", "style"} or ns is not None:
#                 continue
#             new_path.attribs[k] = v

#         style = path_element.get("style")
#         if style:
#             new_path.update(parse_style(style))

#         group.add(new_path)

#     dwg.add(group)

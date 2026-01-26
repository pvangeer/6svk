import re
from svgwrite import Drawing


def draw_disclaimer(
    dwg: Drawing,
    disclaimer_text: str,
    insert: tuple[float, float],
    dominant_baseline: str = "hanging",
    text_anchor: str = "start",
    font_size: float = 12,
    links: list[tuple[str, str]] = [],
):
    pattern = f"({'|'.join(map(re.escape, [l[0] for l in links]))})"
    parts = re.split(pattern, disclaimer_text)

    disclaimer_text_element = dwg.text(
        parts[0],
        insert=insert,
        dominant_baseline=dominant_baseline,
        text_anchor=text_anchor,
        font_size=font_size,
    )

    for part in parts[1:]:
        link_tuple = next((t for t in links if t[0] == part), None)
        if link_tuple is not None:
            link = dwg.a(link_tuple[1])

            link.add(
                dwg.tspan(
                    link_tuple[0],
                    fill="blue",
                    text_decoration="underline",
                    cursor="pointer",
                )
            )

            disclaimer_text_element.add(link)
        else:
            disclaimer_text_element.add(dwg.tspan(part, font_size=font_size))

    dwg.add(disclaimer_text_element)

from svgwrite import Drawing
from svk.visualization.helpers.icons import BarrierIcons
from svk.visualization.helpers import draw_scaled_icon
from svk.io import svg_to_pdf


def test_draw_icon():
    dwg = Drawing(size=("100px", "100px"))
    draw_scaled_icon(dwg, icon=BarrierIcons.MaeslantBarrier, insert=(55, 10), size=(12, 12))
    draw_scaled_icon(dwg, icon=BarrierIcons.MaeslantBarrier, insert=(20, 40), size=(24, 24))
    draw_scaled_icon(dwg, icon=BarrierIcons.MaeslantBarrier, insert=(10, 70), size=(6, 6))
    svg_to_pdf(dwg, "C:/Test/icon.pdf")

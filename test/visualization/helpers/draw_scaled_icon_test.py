from svgwrite import Drawing
from svk.visualization.helpers.icons import BarrierIcons
from svk.visualization.helpers import draw_scaled_icon
from svk.io import svg_to_pdf


def test_draw_icon():
    dwg = Drawing(size=("100px", "100px"))
    draw_scaled_icon(dwg, icon=BarrierIcons.MaeslantBarrier, insert=(5, 10), size=(12, 12))
    draw_scaled_icon(dwg, icon=BarrierIcons.HaringvlietBarrier, insert=(25, 15), size=(24, 24))
    draw_scaled_icon(dwg, icon=BarrierIcons.Ramspol, insert=(80, 30), size=(16, 16))
    draw_scaled_icon(dwg, icon=BarrierIcons.HartelBarrier, insert=(10, 70), size=(35, 35))
    draw_scaled_icon(dwg, icon=BarrierIcons.EasternScheldBarrier, insert=(40, 60), size=(24, 24))
    draw_scaled_icon(dwg, icon=BarrierIcons.HollandseIJsselBarrier, insert=(80, 80), size=(16, 16))
    svg_to_pdf(dwg, "C:/Test/icon.pdf")

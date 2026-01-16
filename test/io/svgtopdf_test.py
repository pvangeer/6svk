from svgwrite import Drawing
from svk.io import svg_to_pdf
from svk.visualization.helpers import chevron
import os


def test_svgtopdf_produces_figure():
    dwg = Drawing(size=("1240px", "800px"))
    dwg.add(chevron(dwg, x=20, y=20, width=400, height=80, id="nu"))
    dwg.add(chevron(dwg, x=420, y=20, width=400, height=80, id="boeggolf"))
    dwg.add(chevron(dwg, x=820, y=20, width=400, height=80, id="toekomst"))
    pt = "C:/test/testimage.pdf"
    if os.path.isfile(pt):
        os.remove(pt)

    svg_to_pdf(dwg, pt)
    assert os.path.isfile(pt)

    # os.remove(pt)

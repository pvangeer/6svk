import svgwrite

from svk.data import LinksRegister, Translator
from svk.io import RendererServer
from svk.visualization import LayoutConfiguration
from svk.visualization.elements._text_element import TextElement


def test_text_element_uses_layout_font_family(monkeypatch):
    measured = {}

    def fake_measure_text(cls, *args, **kwargs):
        measured.update(kwargs)
        return 100, 12

    monkeypatch.setattr(RendererServer, "measure_text", classmethod(fake_measure_text))
    element = TextElement(
        text="Configured font",
        layout_configuration=LayoutConfiguration(font_family="monospace"),
        links_register=LinksRegister(),
        translator=Translator(),
    )
    drawing = svgwrite.Drawing()

    element.draw(drawing, 0, 0)

    assert measured["font_family"] == "monospace"
    assert 'font-family="monospace"' in drawing.tostring()

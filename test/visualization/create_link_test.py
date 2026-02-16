import svgwrite
from svk.io import svg_to_pdf, svg_to_pdf_chrome


def test_create_internal_link():
    # Create an SVG canvas
    dwg = svgwrite.Drawing("example.svg", size=("400px", "200px"))

    # Create a target element with an id
    target_text = dwg.text("Target Section", insert=(50, 150), fill="black", id="target")  # <-- This sets the element id
    dwg.add(target_text)

    # Create a rectangle that will act as a link
    link_rect = dwg.rect(insert=(50, 50), size=(150, 30), fill="blue")
    dwg.add(link_rect)

    # Create text for the clickable rectangle
    link_text = dwg.text("Go to Target", insert=(60, 70), fill="white")
    dwg.add(link_text)

    # Wrap the rect + text in an <a> tag to make it a link
    link = dwg.add(dwg.a(href="#target"))  # internal SVG link
    link.add(link_rect)
    link.add(link_text)

    # svg_to_pdf(dwg, "C:/Test/internal_link_test.pdf")
    svg_to_pdf(dwg, "C:/Test/", "internal_link_via_inkscape")

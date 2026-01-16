from playwright.sync_api import sync_playwright
from svgwrite import Drawing


def svg_to_pdf(svg_dwg: Drawing, pdf_path: str):
    """
    Save an svgwrite.Drawing object to PDF with all effects and links preserved.

    Parameters:
    -----------
    svg_dwg : svgwrite.Drawing
        The svgwrite SVG object to export.
    pdf_path : str
        Path to the output PDF file.
    """
    # Convert SVG to string
    svg_content = svg_dwg.tostring()

    # Wrap the SVG in minimal HTML
    html = f"""
    <html>
      <body style="margin:0; padding:0;">
        {svg_content}
      </body>
    </html>
    """

    with sync_playwright() as p:
        browser = p.chromium.launch()  # headless by default
        page = browser.new_page()

        page.set_content(html)

        # Save PDF, using the SVG's width/height if set
        width = str(svg_dwg.attribs.get("width")) if "width" in svg_dwg.attribs else "800px"
        height = str(svg_dwg.attribs.get("height")) if "height" in svg_dwg.attribs else "600px"

        page.pdf(path=pdf_path, width=width, height=height, print_background=True)

        browser.close()

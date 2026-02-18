from PyPDF2 import PdfMerger
from svk.data import LinksRegister
import fitz


def merge_pdf_files(input_files: list[str], output_file: str):
    merger = PdfMerger()

    for pdf in input_files:
        merger.append(pdf)

    merger.write(output_file)
    merger.close()


def _scale_coordinates(x: float, y: float, svg_width: float, svg_height: float, pdf_width: float, pdf_height: float):
    x_pdf = x * pdf_width / svg_width
    y_pdf = y * pdf_height / svg_height
    return x_pdf, y_pdf


def add_links(input_pdf_file: str, output_file: str, links_manager: LinksRegister):
    doc = fitz.open(input_pdf_file)
    links = links_manager.links
    link_targets = links_manager.link_targets
    svg_sizes = links_manager.page_sizes

    for target_id in links.keys() & link_targets.keys():
        links_list = links[target_id]
        target = link_targets[target_id]
        target_page_index = target[0]
        target_pdf_page = doc[target_page_index]
        x_target, y_target = _scale_coordinates(
            target[1],
            target[2],
            svg_sizes[target_page_index][0],
            svg_sizes[target_page_index][1],
            target_pdf_page.rect.width,
            target_pdf_page.rect.height,
        )
        target_point = fitz.Point(x_target, y_target)

        for link in links_list:
            source_page_index = link[0]
            svg_size = svg_sizes[source_page_index]
            p = doc[source_page_index]
            pdf_width, pdf_height = p.rect.width, p.rect.height
            x_left_up, y_left_up = _scale_coordinates(link[1], link[2], svg_size[0], svg_size[1], pdf_width, pdf_height)
            x_right_down, y_right_down = _scale_coordinates(
                link[1] + link[3], link[2] + link[4], svg_size[0], svg_size[1], pdf_width, pdf_height
            )
            rect = fitz.Rect(x_left_up, y_left_up, x_right_down, y_right_down)
            doc[source_page_index].insert_link(
                {
                    "kind": fitz.LINK_GOTO,
                    "from": rect,
                    "page": target_page_index,
                    "to": target_point,
                    "border": [2, 2, 2],
                    "color": (1, 0, 0),
                }
            )

    doc.save(output_file)
    doc.close()

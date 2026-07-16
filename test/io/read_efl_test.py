from svk.io import EndOfLifeDatabase, svg_to_pdf_chrome
from svk.visualization import EndOfLifePage, LayoutConfiguration
from svk.data import StormSurgeBarrier, LinksRegister, Translator


def test_read_efl_database():
    """
    Test function for the EFL database. It reads the database file and prints the data.

    :return: None
    """

    d = EndOfLifeDatabase(
        "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK/03 HV/01 Uitwerking/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"
    )
    d.read()
    assert d.grid is not None
    assert len(d.grid.cells) > 0
    assert len(d.grid.column_headers) > 0
    assert len(d.grid.row_headers) > 0


def test_first_try_efl_page():
    d = EndOfLifeDatabase(
        "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK/03 HV/01 Uitwerking/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"
    )
    d.read()
    assert d.grid is not None

    page = EndOfLifePage(
        page_number=2,
        title="EOL",
        icon=StormSurgeBarrier.HaringvlietBarrier,
        layout_configuration=LayoutConfiguration(),
        links_register=LinksRegister(),
        translator=Translator(),
        grid=d.grid,
    )
    dwg = page.draw()
    pt = "C:/test/EOL.pdf"
    svg_to_pdf_chrome(dwg, pt)

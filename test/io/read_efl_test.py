from svk.io import EndOfLifeDatabase


def test_read_efl_database():
    """
    Test function for the EFL database. It reads the database file and prints the data.

    :return: None
    """

    d = EndOfLifeDatabase(
        "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK/03 HV/01 Uitwerking/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"
    )
    d.read()
    assert len(d.cells) > 0
    assert len(d.functions) > 0
    assert len(d.drivers) > 0

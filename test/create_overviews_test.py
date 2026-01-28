from svk.io import Database
from svk.visualization import create_image_from_database
from svk.visualization.helpers.icons import BarrierIcons
from datetime import datetime

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"


def convert_database(database_path, title, barrier_icon, output_dir):
    now = datetime.now().strftime("%Y-%m-%d")

    print(f"Read questions from database: {database_path }")
    questions = Database(database_path)
    questions.read()

    for e in questions.errors:
        print(f"{e.cell_reference}: {str(e)}")

    target_file_path = f"{output_dir}/{now} - Kennisvragen {title}.pdf"
    print(f"create image: {target_file_path}")
    create_image_from_database(
        title,
        questions,
        target_file_path,
        barrier_icon=barrier_icon,
    )


def test_create_overview_hv():
    hv_dir = base_dir + "/03 HV/01 Uitwerking"
    convert_database(
        database_path=hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx",
        title="Haringvlietsluizen",
        barrier_icon=BarrierIcons.HaringvlietBarrier,
        output_dir=hv_dir,
    )


def test_create_overview_rp():
    rp_dir = base_dir + "/07 RP/01 Uitwerking"
    convert_database(
        database_path=rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx",
        title="Ramspol",
        barrier_icon=BarrierIcons.Ramspol,
        output_dir=rp_dir,
    )


def test_create_overview_hijk():
    hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
    convert_database(
        database_path=hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx",
        title="Hollandse IJssel Kering",
        barrier_icon=BarrierIcons.HollandseIJsselBarrier,
        output_dir=hijk_dir,
    )

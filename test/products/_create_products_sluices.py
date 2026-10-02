from datetime import datetime
from pathlib import Path
from svk.visualization import SluicesDocument
from test.utils.database_reader import read_ph_database


def create_sluices_overview(output_dir: Path):
    questions = read_ph_database()
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda Sluis Panheel"

    calendar = SluicesDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        cleanup=True,
    )

    calendar.build()

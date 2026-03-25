from datetime import datetime
from typing import cast

from svk.io import ImpactPathwayDatabase
from svk.visualization import ImpactPathwayDocument
from svk.data import ResearchQuestion


def test_plot_pathway():
    impact_dir = "C:/Test/"
    database_path = impact_dir + "/SSB-delta_impact-pathway-database.xlsx"
    output_dir = impact_dir

    d = ImpactPathwayDatabase(database_path)
    d.read()
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Impact pathway SSB-delta"

    pathway = ImpactPathwayDocument(questions=cast(list[ResearchQuestion], d), output_dir=output_dir, output_file=output_file)
    pathway.build()

from datetime import datetime
from typing import cast

from svk.io import ImpactPathwayDatabase
from svk.visualization import ImpactPathwayDocument
from svk.data import StormSurgeBarrierResearchQuestion
from test.paths import test_data_dir, test_output_dir


def test_plot_pathway():
    database_path = test_data_dir + "/example-SSB-2.xlsx"

    d = ImpactPathwayDatabase(database_path)
    d.read()
    questions = [q for q in d if q.action_holder != "Not included"]
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Impact pathway SSB-delta"

    pathway = ImpactPathwayDocument(
        questions=cast(list[StormSurgeBarrierResearchQuestion], questions), output_dir=test_output_dir, output_file=output_file
    )
    pathway.build()

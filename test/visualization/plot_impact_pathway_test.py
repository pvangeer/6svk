from svk.io import ImpactPathwayDatabase
from svk.visualization import ImpactPathway
from typing import cast
from svk.data import ResearchQuestion


def test_plot_pathway():
    d = ImpactPathwayDatabase("C:/src/6svk/test/test-data/example-SSB-delta.xlsx")
    d.read()
    pathway = ImpactPathway(questions=cast(list[ResearchQuestion], d), output_dir="C:/Test/", output_file="Impact_pathway_test")
    pathway.build()

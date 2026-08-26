from svk.data import StormSurgeBarrier, Grid
from svk.visualization.pages._lifetime_analysis_page import LifeTimeAnalysisPage
from svk.visualization.documents._document import Document
from svk.visualization.pages._page import Page


class LifeTimeAnalysDocument(Document):
    storm_surge_barrier: StormSurgeBarrier
    disclaimer: str | None = (
        "Dit is een eerste concept van de onderzoeksagenda stormvloedkeringen. Deze versie is ontstaan in samenwerking met de asset management teams van de keringen. De prioritering van de onderzoeksvragen moet nog gereviewd worden door o.a. de asset management teams en RWS WVL/GPO. De indeling in tijdsperiode is op dit moment in ontwikkeling. Voor vragen, neem contact op met Marit de Jong of Riva de Vries."
    )
    disclaimer_links: list[tuple[str, str]] | None = [
        ("Riva de Vries", "mailto:riva.de.vries@rws.nl"),
        ("Marit de Jong", "mailto:marit.de.jong@rws.nl"),
    ]
    functional_lifetime_grid: Grid
    technical_lifetime_grid: Grid

    def create_pages(self) -> list[Page]:
        return [
            LifeTimeAnalysisPage(
                page_number=0,
                title=f"EFL - {self.translator.get_label(self.storm_surge_barrier.title)}",
                layout_configuration=self.layout_configuration,
                links_register=self.links_register,
                translator=self.translator,
                icon=self.storm_surge_barrier,
                disclaimer=self.disclaimer,
                disclaimer_links=self.disclaimer_links,
                grid=self.functional_lifetime_grid,
            ),
            LifeTimeAnalysisPage(
                page_number=0,
                title=f"ETL - {self.translator.get_label(self.storm_surge_barrier.title)}",
                layout_configuration=self.layout_configuration,
                links_register=self.links_register,
                translator=self.translator,
                icon=self.storm_surge_barrier,
                disclaimer=self.disclaimer,
                disclaimer_links=self.disclaimer_links,
                grid=self.technical_lifetime_grid,
            ),
        ]

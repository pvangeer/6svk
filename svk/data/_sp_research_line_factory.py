from pydantic import BaseModel
from svk.data._research_line import ResearchLine
from svk.data._sp_research_lines import SluicesResearchLines

darkblue = (16, 49, 86)
sandy = (107, 96, 3)
grey = (127, 127, 127)


class SluicesResearchLineFactory(BaseModel):
    @staticmethod
    def get_sp_research_line_from_str(title: str) -> SluicesResearchLines:
        match title:
            case "Technische levensduur - civiele delen":
                return SluicesResearchLines.TechnicalLifeTimeCivilParts
            case "Technische levensduur - installaties":
                return SluicesResearchLines.TechnicalLifeTimeInstallations
            case "Inspecties, monitoring en data":
                return SluicesResearchLines.InspectionsMonitoringAndData
            case "Hoogwaterveiligheid":
                return SluicesResearchLines.WaterSafety
            case "Watersysteem en waterbeschikbaarheid":
                return SluicesResearchLines.WaterSystemAndAvailability
            case "Ecologie en waterkwaliteit watersysteem":
                return SluicesResearchLines.EcologyAndWaterQuality
            case "Functies van het complex in het netwerk (scheepvaart, weg en water)":
                return SluicesResearchLines.Functions
            case "Operatie: bediening en besturing":
                return SluicesResearchLines.Operation
            case "Beschikbaarheid en robuustheid":
                return SluicesResearchLines.Robustness
            case "Stategie, afweging en keuzes":
                return SluicesResearchLines.Strategy
            case "Milieu-impact":
                return SluicesResearchLines.EnvironmentalImpact
            case "Organisatorische aspecten":
                return SluicesResearchLines.Organizational
            case _:
                raise ValueError("Unknown research line")

    @staticmethod
    def get_sp_research_line_from_int(number: int) -> SluicesResearchLines:
        match number:
            case 1:
                return SluicesResearchLines.TechnicalLifeTimeCivilParts
            case 2:
                return SluicesResearchLines.TechnicalLifeTimeInstallations
            case 3:
                return SluicesResearchLines.InspectionsMonitoringAndData
            case 4:
                return SluicesResearchLines.WaterSafety
            case 5:
                return SluicesResearchLines.WaterSystemAndAvailability
            case 6:
                return SluicesResearchLines.EcologyAndWaterQuality
            case 7:
                return SluicesResearchLines.Functions
            case 8:
                return SluicesResearchLines.Operation
            case 9:
                return SluicesResearchLines.Robustness
            case 10:
                return SluicesResearchLines.Strategy
            case 11:
                return SluicesResearchLines.EnvironmentalImpact
            case 12:
                return SluicesResearchLines.Organizational
            case _:
                raise ValueError("Unknown research line")

    @staticmethod
    def get_research_line_from_int(number: int) -> ResearchLine:
        """
        This method returns a research line object associated to a particular research line number.

        :param number: The number associated to the desired research line.
        :type number: int
        :return: The associated research line.
        :rtype: ResearchLine
        """
        return SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLineFactory.get_sp_research_line_from_int(number))

    @staticmethod
    def get_research_line_from_str(title: str) -> ResearchLine:
        """
        This method returns a research line object associated to a particular research title.

        :param title: The title associated to the desired research line.
        :type title: str
        :return: The associated research line.
        :rtype: ResearchLine
        """
        return SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLineFactory.get_sp_research_line_from_str(title))

    @staticmethod
    def get_research_line_from_ssb_enum(storm_surge_barrier_research_line: SluicesResearchLines) -> ResearchLine:
        return ResearchLine(
            number=storm_surge_barrier_research_line.number,
            title=storm_surge_barrier_research_line.title,
            cluster=storm_surge_barrier_research_line.cluster,
            base_color=SluicesResearchLineFactory.get_base_color(storm_surge_barrier_research_line.cluster),
        )

    @staticmethod
    def get_base_color(cluster) -> tuple[int, int, int]:
        """
        Returns the R, G and B values of the color associated to the color group of the research line. R,G and B are integers ranging from 0 - 256.

        :return: R,G,B of the associated color.
        :rtype: tuple[int, int, int]
        """
        match cluster:
            case 1:
                return darkblue
            case 2:
                return sandy
            case 3:
                return grey
        raise ValueError("Unknown color group.")

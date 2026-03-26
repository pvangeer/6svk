"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the 6svk toolbox.

This program is free software; you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this
program; if not, see <https://www.gnu.org/licenses/>.

All names, logos, and references to "Deltares" are registered trademarks of Stichting
Deltares and remain full property of Stichting Deltares at all times. All rights reserved.
"""

from svk.data import ResearchQuestion, ImpactPathwayResearchQuestion, TimeFrame
from svk.visualization.helpers._greyfraction import color_toward_grey


def get_priority_2(question: ImpactPathwayResearchQuestion) -> int:
    prios = [
        question.prio_management_maintenance,
        question.prio_operation,
        question.prio_other_functions,
        question.prio_urgency_decision_making,
        question.prio_water_safety,
    ]
    combined_priority = sum([p.id for p in prios])
    n_high_prio = sum(1 for p in prios if p.id == 3)
    if n_high_prio > 1 or combined_priority > 10:
        return 3
    if n_high_prio > 0 or combined_priority > 8:
        return 2
    return 1


def get_subtitle(time_frame: TimeFrame) -> str:
    match time_frame:
        case TimeFrame.Now:
            return ""
        case TimeFrame.NearFuture:
            return "(2033 - 2040)"
        case TimeFrame.Future:
            return "(>2040)"
        case TimeFrame.NotRelevant:
            return "(-)"
        case TimeFrame.Unknown:
            return "(?)"
        case _:
            raise ValueError("Unknown time frame")


def get_header_color(time_frame: TimeFrame) -> str:
    return color_toward_grey((18, 103, 221), grey_fraction=time_frame.grey_fraction)

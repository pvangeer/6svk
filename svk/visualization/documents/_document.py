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

import os
from pydantic import BaseModel
from abc import ABC, abstractmethod
from collections import defaultdict
from svk.data import ResearchQuestion, LinksRegister, ResearchLine, Translator, TimeFrame, Label
from svk.io import svg_to_pdf_chrome, merge_pdf_files, add_links
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization.pages._time_line_overview_page import TimeLineOverviewPage
from svk.visualization.pages._details_page import DetailsPage
from svk.visualization.elements._question_details import QuestionDetailsElement
from svk.visualization.pages._page import Page
from svk.visualization.elements._column import Column


class Document(BaseModel, ABC):
    layout_configuration: LayoutConfiguration = LayoutConfiguration()
    links_register: LinksRegister = LinksRegister()
    translator: Translator = Translator(lang="nl")
    questions: list[ResearchQuestion]
    pages: list[Page] = []
    output_dir: str
    output_file: str
    disclaimer: str | None = None
    disclaimer_links: list[tuple[str, str]] | None = None
    cleanup: bool = True
    """When set to false, intermediate files are left in the output dir."""
    _str_table = str.maketrans({".": "-", " ": "-"})

    @abstractmethod
    def create_pages(self) -> list[Page]:
        return self.create_detailes_pages(current_page_number=1)

    def build(self):
        self.pages = self.create_pages()

        all_files = self._convert_pages_to_pdf()

        no_links_output_file = os.path.join(self.output_dir, self.output_file + " - no links.pdf")
        merge_pdf_files(all_files, no_links_output_file)

        # TODO: This assumes all page numbers are correct.
        output_file_final = os.path.join(self.output_dir, self.output_file + ".pdf")
        add_links(no_links_output_file, output_file_final, self.links_register)

        if self.cleanup:
            for file in all_files:
                if os.path.exists(file):
                    os.remove(file)
            if os.path.exists(no_links_output_file):
                os.remove(no_links_output_file)

        return output_file_final

    def create_detailes_pages(self, current_page_number: int) -> list[Page]:
        pages: list[Page] = []

        grouped_questions: defaultdict[ResearchLine, list[ResearchQuestion]] = defaultdict(list[ResearchQuestion])
        non_grouped: list[ResearchQuestion] = []
        for question in self.questions:
            if question.research_line_primary is None:
                non_grouped.append(question)
            else:
                grouped_questions[question.research_line_primary].append(question)

        for research_line in sorted(grouped_questions, key=lambda r_l: r_l.number):
            pages.append(
                self.create_details_page(
                    page_number=current_page_number,
                    title=str(research_line.number) + ". " + self.translator.get_label(research_line.title),
                    link_target=research_line.id,
                    questions=grouped_questions[research_line],
                )
            )
            current_page_number += 1

        if len(non_grouped) > 0:
            pages.append(
                self.create_details_page(
                    page_number=current_page_number,
                    title=self.translator.get_label(Label.D_NoResearchLine),
                    link_target="",
                    questions=non_grouped,
                )
            )

        return pages

    def add_time_frame_column(self, fig: TimeLineOverviewPage, time_frame: TimeFrame, number: int):
        column = Column(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            header_title=self.translator.get_label(time_frame.description),
            header_subtitle=helper.get_subtitle(time_frame),
            header_color=helper.get_header_color(time_frame),
            number=number,
        )

        fig.columns.append(column)

    def create_details_page(
        self,
        page_number: int,
        title: str,
        link_target: str,
        questions: list[ResearchQuestion],
    ) -> Page:
        dwg_details_page = DetailsPage(
            page_number=page_number,
            title=title,
            title_link_target=link_target,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
        )
        for question in sorted(questions, key=lambda q: q.id):
            dwg_details_page.questions.append(
                QuestionDetailsElement(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    research_question=question,
                )
            )

        return dwg_details_page

    def _convert_pages_to_pdf(self) -> list[str]:
        pages_file_paths: list[str] = []
        for page in sorted(self.pages, key=lambda p: p.page_number):
            target_path = os.path.join(self.output_dir, self.output_file + "-" + page.title.translate(self._str_table) + ".pdf")
            svg_to_pdf_chrome(svg_dwg=page.draw(), pdf_path=target_path)
            pages_file_paths.append(target_path)

        return pages_file_paths

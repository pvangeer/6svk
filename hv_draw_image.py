from svk.io import Database, svg_to_pdf
from svk.data import TimeFrame, ResearchQuestion
from svk.visualization import Figure, Column, Group, Question, create_image_from_database
from collections import defaultdict


hv_questions = Database("C:/src/6svk/examples/Example-HV.xlsx")
hv_questions.read()
for e in hv_questions.errors:
    print(f"{e.cell_reference}: {str(e)}")

create_image_from_database(hv_questions, "C:/Test/Example-HV.pdf")

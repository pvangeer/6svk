from svk.io import Database
from svk.visualization import create_image_from_database

hv_questions = Database("C:/src/6svk/examples/Example-HV.xlsx")
hv_questions.read()

for e in hv_questions.errors:
    print(f"{e.cell_reference}: {str(e)}")

create_image_from_database(hv_questions, "C:/Test/Example-HV.pdf")

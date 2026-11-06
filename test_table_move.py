import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = docx.Document(r"c:\Users\Admin\Downloads\Plantilla - Reporte final de pruebas.docx")
p_intro = None
for p in doc.paragraphs:
    if "INTRODUCCI" in p.text:
        p_intro = p
        break

# Create table
tbl = doc.add_table(rows=2, cols=2)
tbl.cell(0, 0).text = "Col 1"
tbl.cell(0, 1).text = "Col 2"
tbl.cell(1, 0).text = "Val 1"
tbl.cell(1, 1).text = "Val 2"

# Move table after p_intro
p_intro._p.addnext(tbl._tbl)

doc.save("test_table_move.docx")
print("Table move successful.")

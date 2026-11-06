import docx
from docx.oxml import OxmlElement
from docx.shared import Inches, Pt, RGBColor

def insert_p_after(ref_p, text="", style='Normal'):
    new_p = OxmlElement('w:p')
    ref_p._p.addnext(new_p)
    doc_p = docx.text.paragraph.Paragraph(new_p, ref_p._parent)
    if style:
        doc_p.style = style
    if text:
        doc_p.add_run(text)
    return doc_p

doc = docx.Document(r"c:\Users\Admin\Downloads\Plantilla - Reporte final de pruebas.docx")
p_intro = None
for p in doc.paragraphs:
    if "INTRODUCCI" in p.text:
        p_intro = p
        break

if p_intro:
    p_added = insert_p_after(p_intro, "Este es un párrafo de prueba insertado inmediatamente después de INTRODUCCIÓN.")
    print("Success: paragraph inserted after INTRODUCCIÓN")

doc.save("test_insert.docx")
print("Saved test_insert.docx successfully.")

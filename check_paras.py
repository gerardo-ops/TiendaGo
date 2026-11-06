import docx

doc = docx.Document(r"c:\Users\Admin\Downloads\Plantilla - Reporte final de pruebas.docx")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"P{i:02d}: '{p.text}' (style: {p.style.name})")

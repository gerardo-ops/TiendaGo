import docx

doc = docx.Document("Reporte_Final_de_Pruebas_TiendaGo_Grupo06.docx")
print("Total paragraphs:", len(doc.paragraphs))
print("Total tables:", len(doc.tables))
print("Total sections:", len(doc.sections))

# Check images
img_count = 0
for rel in doc.part.rels.values():
    if "image" in rel.target_ref:
        img_count += 1
print("Embedded images:", img_count)

# Check some sample paragraphs to confirm text presence
print("\n--- Sample Paragraphs ---")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() and i < 30:
        print(f"P{i:02d}: {p.text[:80]}...")

print("\n--- Table sizes ---")
for i, t in enumerate(doc.tables):
    print(f"Table {i}: rows={len(t.rows)}, cols={len(t.columns)}")

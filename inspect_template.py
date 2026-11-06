import docx

doc = docx.Document(r"c:\Users\Admin\Downloads\Plantilla - Reporte final de pruebas.docx")
print("Total paragraphs:", len(doc.paragraphs))
for i, p in enumerate(doc.paragraphs):
    sdts = p._p.xpath('.//w:sdt')
    alias = [s.xpath('.//w:alias/@w:val') for s in sdts]
    t_text = "".join(p._p.xpath('.//w:t/text()'))
    print(f"P{i:02d} [{p.style.name}]: text='{p.text}' | raw_t='{t_text}' | sdt_aliases={alias}")

print("Total tables:", len(doc.tables))
for i, t in enumerate(doc.tables):
    print(f"Table {i}: rows={len(t.rows)}, cols={len(t.columns)}")
    for r_idx, r in enumerate(t.rows):
        r_text = [c.text.strip().replace('\n', ' ') for c in r.cells]
        print(f"  R{r_idx}: {r_text}")

# Check headers and footers
for s_idx, sec in enumerate(doc.sections):
    print(f"Section {s_idx}:")
    h_text = ["".join(p._p.xpath('.//w:t/text()')) for p in sec.header.paragraphs]
    f_text = ["".join(p._p.xpath('.//w:t/text()')) for p in sec.footer.paragraphs]
    print("  Header text:", h_text)
    print("  Footer text:", f_text)

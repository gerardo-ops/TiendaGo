import docx

doc = docx.Document(r"c:\Users\Admin\Downloads\Plantilla - Reporte final de pruebas.docx")
body = doc._body._element
T_TAG = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'

def set_sdt_text(sdt_elem, new_text):
    # Find sdtContent
    content = sdt_elem.xpath('.//*[local-name()="sdtContent"]')
    if not content:
        return
    t_nodes = content[0].xpath('.//*[local-name()="t"]')
    if t_nodes:
        t_nodes[0].text = new_text
        for node in t_nodes[1:]:
            node.text = ""
    # remove showingPlcHdr if present
    plc = sdt_elem.xpath('.//*[local-name()="showingPlcHdr"]')
    for p in plc:
        p.getparent().remove(p)

# Test updating SDT [05] (Carrera)
for child in body:
    if child.tag.endswith('sdt'):
        alias = child.xpath('.//*[local-name()="alias"]/@*[local-name()="val"]')
        if alias and alias[0] == 'Nombre Carrera':
            set_sdt_text(child, "TÉCNICO EN INGENIERÍA DE DESARROLLO DE SOFTWARE")
            print("Updated Nombre Carrera!")

doc.save("test_template_mod.docx")
print("Saved test_template_mod.docx successfully.")

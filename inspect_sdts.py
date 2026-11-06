import docx

doc = docx.Document(r"c:\Users\Admin\Downloads\Plantilla - Reporte final de pruebas.docx")
body = doc._body._element
T_TAG = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'

print("--- SDT Details in Body ---")
for i, child in enumerate(body):
    tag = child.tag.split('}')[-1]
    if tag == 'sdt':
        alias = child.xpath('.//*[local-name()="alias"]/@*[local-name()="val"]')
        tag_val = child.xpath('.//*[local-name()="tag"]/@*[local-name()="val"]')
        t_nodes = [elem.text for elem in child.iter(T_TAG) if elem.text]
        text_content = "".join(t_nodes)
        print(f"Child [{i:02d}] SDT: alias={alias} tag={tag_val} text='{text_content}'")
    else:
        t_nodes = [elem.text for elem in child.iter(T_TAG) if elem.text]
        text_content = "".join(t_nodes)
        if text_content.strip():
            print(f"Child [{i:02d}] <{tag}>: text='{text_content}'")

print("\n--- Headers SDT Details ---")
for s_idx, sec in enumerate(doc.sections):
    sdts = sec.header._element.xpath('.//*[local-name()="sdt"]')
    for s in sdts:
        alias = s.xpath('.//*[local-name()="alias"]/@*[local-name()="val"]')
        t_nodes = [elem.text for elem in s.iter(T_TAG) if elem.text]
        print(f"Sec {s_idx} header SDT: alias={alias} text='{''.join(t_nodes)}'")

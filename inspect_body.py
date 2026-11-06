import docx

doc = docx.Document(r"c:\Users\Admin\Downloads\Plantilla - Reporte final de pruebas.docx")
body = doc._body._element
T_TAG = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'

print("Children of body:")
for i, child in enumerate(body):
    tag = child.tag.split('}')[-1]
    t_nodes = [elem.text for elem in child.iter(T_TAG) if elem.text]
    snippet = "".join(t_nodes)[:70].replace('\n', ' ')
    print(f"[{i:02d}] <{tag}>: text='{snippet}'")

print("\n--- Header / Footer inspection ---")
for s_idx, sec in enumerate(doc.sections):
    h_children = [c.tag.split('}')[-1] for c in sec.header._element]
    f_children = [c.tag.split('}')[-1] for c in sec.footer._element]
    h_text = "".join([elem.text for elem in sec.header._element.iter(T_TAG) if elem.text]).replace('\n', ' ')
    f_text = "".join([elem.text for elem in sec.footer._element.iter(T_TAG) if elem.text]).replace('\n', ' ')
    print(f"Sec {s_idx}: header tags={h_children} text='{h_text}' | footer tags={f_children} text='{f_text}'")

import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def parse_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    sections = re.split(r'\n\*\*([IVXLCDM]+\. .*?)\*\*', content)
    parsed = {}
    for i in range(1, len(sections), 2):
        title = sections[i].strip()
        body = [line.strip().lstrip("* ") for line in sections[i+1].strip().split('\n') if line.strip()]
        parsed[title] = body
    return parsed

def generate_pdf(content, filename="output.pdf", sections=False):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)

    if sections:
        def section(title, items):
            parts = [Paragraph(f'<b>{title}</b>', styles["Heading2"])]
            parts += [Paragraph(f'• {item}', styles["Normal"]) for item in items]
            parts.append(Spacer(1, 12))
            return parts
        body = []
        for title, items in content.items():
            body.extend(section(title, items))
        doc.build(body)
    else:
        if isinstance(content, str): content = content.split('\n')
        body = [Paragraph(line, styles["BodyText"]) for line in content if line.strip()]
        doc.build(body)

def convert_to_pdf(input_file, pdf_path, parse):
    if parse:
        parsed = parse_text_file(input_file)
        generate_pdf(parsed, pdf_path, sections=True)
    else:
        with open(input_file, 'r') as f:
            generate_pdf(f.read(), pdf_path, sections=False)

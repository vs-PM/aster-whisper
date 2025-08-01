import re
from datetime import datetime

from docx import Document

MONTHS = [
    '', 'января', 'февраля', 'марта', 'апреля', 'мая',
    'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
]

def format_russian_date(value):
    if isinstance(value, str):
        try:
            val = datetime.fromisoformat(value)
        except Exception:
            return value
    elif isinstance(value, datetime):
        val = value
    else:
        return value
    day = val.day
    month = MONTHS[val.month]
    year = val.year
    return f"{day:02d} {month} {year} года"


def extract_tags_from_docx(template_path: str):
    doc = Document(template_path)
    tags = set()
    pattern = re.compile(r'{(\w+)}')
    for paragraph in doc.paragraphs:
        tags.update(pattern.findall(paragraph.text))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                tags.update(pattern.findall(cell.text))
    return list(tags)


def replace_placeholder_in_paragraph(paragraph, values: dict):
    pattern = re.compile(r'{(\w+)}')
    for key, val in values.items():
        placeholder = f"{{{key}}}"
        if placeholder in paragraph.text:
            inline = paragraph.runs
            for i in range(len(inline)):
                if placeholder in inline[i].text:
                    inline[i].text = inline[i].text.replace(placeholder, str(val))
            paragraph.text = paragraph.text.replace(placeholder, str(val))


def replace_placeholders_in_table(table, values: dict):
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                replace_placeholder_in_paragraph(paragraph, values)


def generate_filled_docx(template_path: str, output_path: str, values: dict):
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        replace_placeholder_in_paragraph(paragraph, values)
    for table in doc.tables:
        replace_placeholders_in_table(table, values)
    doc.save(output_path)

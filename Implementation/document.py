import os

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from formatter import coordinates_to_lines

def __remove_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr

    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'nil')
        tblBorders.append(border)

    tblPr.append(tblBorders)

def create_document(contents: list[list[str | list]], output_path: str, debug: bool = False) -> None:
    if debug:
        print("Rozpoczęcie tworzenia dokumentu programu MS Word")

    lines = coordinates_to_lines(contents, debug)

    doc = Document()

    last_y: int = 0
    last_x: int = 0
    buffer: list[str] = []
    table = None
    table_cols = 0

    for line in lines:
        translated: str = line[1]
        coords: tuple[int, int, int] = line[2]
        cur_y: int = coords[0]
        cur_x: int = coords[1]
        font_size: int = coords[2]

        if cur_y != last_y:
            if len(buffer) == 1:
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(buffer[0].strip())
                run.font.size = Pt(font_size)
            else:
                row_length = len(buffer)

                if table is None or row_length != table_cols:
                    table = doc.add_table(rows=1, cols=row_length)
                    __remove_table_borders(table)
                    table.style = 'Table Grid'
                    table_cols = row_length
                    row_cells = table.rows[0].cells
                else:
                    row_cells = table.add_row().cells

                for index, text in enumerate(buffer):
                    row_cells[index].text = text.strip()

            buffer = []

        buffer.append(translated)

        last_x = cur_x
        last_y = cur_y

    if buffer:
        if len(buffer) == 1:
            doc.add_paragraph(buffer[0].strip())
        else:
            row_length = len(buffer)
            if table is None or row_length != table_cols:
                table = doc.add_table(rows=1, cols=row_length)
                __remove_table_borders(table)
                table.style = 'Table Grid'
                table_cols = row_length
                row_cells = table.rows[0].cells
            else:
                row_cells = table.add_row().cells

            for index, text in enumerate(buffer):
                row_cells[index].text = text.strip()

    doc.save(output_path)

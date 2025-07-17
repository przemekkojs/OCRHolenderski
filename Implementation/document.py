import os

from docx import Document

def create_document(contents:list[list[str | list]], output_path:str, debug:bool=False) -> None:
    doc = Document(output_path) if os.path.exists(output_path) else Document()

    for line in contents:
        translated:str = line[2]
        doc.add_paragraph(translated)

    doc.save(output_path)

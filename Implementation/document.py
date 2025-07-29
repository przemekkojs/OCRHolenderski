import os
from docx import Document

from formatter import coordinates_to_lines

def create_document(contents:list[list[str | list]], output_path:str, debug:bool=False) -> None:
    if debug:
        print("Rozpoczęcie tworzenia dokumentu programu MS Word")

    lines = coordinates_to_lines(contents, debug)

    doc = Document() #Document(output_path) if os.path.exists(output_path) else Document()

    last_y:int = 0
    last_x:int = 0
    buffer:str = ""

    for line in lines:
        translated:str = line[1]
        
        coords:tuple[int, int, int] = line[2]
        cur_y:int = coords[0]
        cur_x:int = coords[1]
        font_size:int = coords[2]

        if cur_y != last_y:
            doc.add_paragraph(buffer.strip())
            buffer = translated
        else:
            if buffer != "" and cur_x != last_x:
                buffer += '\t\t'
            
            buffer += translated

        last_x = cur_x
        last_y = cur_y            

    doc.save(output_path)

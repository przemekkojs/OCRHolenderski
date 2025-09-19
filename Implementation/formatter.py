from complex_types import alignment, layout_row, row
from font_functions import *

def __detect_font_size(current_row:row, func=fibonacci, debug:bool=False) -> int:
    rect:list[int] = current_row.rect
    lines:int = current_row.lines

    y_min:int = rect[2]
    y_max:int = rect[3]

    diff:int = abs(y_max - y_min) / lines
    bucket:int = int((diff) / 10)
    result:int = func(bucket)

    if debug:
        print(f'Wykryto rozmiar czcionki między [{y_min}, {y_max}]: {diff}, {bucket}, rozmiar: {result}')

    return result
    # return 11

def __detect_alignment(rect:list[int], sheet_size:int=1240, margin:int=300, debug:bool=False) -> alignment:
    x_min:int = int(rect[0])
    x_max:int = int(rect[1])

    avg:int = (x_min + x_max) / 2
    window_avg:int = sheet_size / 2
    tolerated_range:int = (window_avg - margin, window_avg + margin)

    if avg >= tolerated_range[0] and avg <= tolerated_range[1] and x_min >= margin:
        return alignment('C')
    elif avg >= tolerated_range[1]:
        return alignment('R')

    return alignment('L')

def __prepare_for_processing(input_data:list[row], debug:bool = False) -> list[row]:    
    input_data.sort(key=lambda x: (x.rect[2], x.rect[0]))
    return input_data

def __create_layout(sorted_input:list[row], debug: bool = False):
    result_tmp:list[layout_row] = []
    last_line: (row | None) = None
    line_changed:bool = False

    for index, current_line in enumerate(sorted_input):
        if index == 1:
            last_line = sorted_input[0]
        elif line_changed and index > 1:
            last_line = sorted_input[index - 1]
            line_changed = False

        last_result_line:(layout_row | None) = result_tmp[index - 1] if result_tmp else None
        prev_y_index:int = 0 if last_result_line is None else last_result_line.document_row
        current_coords:list[int] = current_line.rect
        buffer:int = 0

        if last_line is not None:            
            last_coords:list[int] = last_line.rect
            cur_y_min:int = current_coords[2]
            last_y_max:int = last_coords[3]

            if cur_y_min >= last_y_max:
                buffer:int = prev_y_index + 1
                line_changed = True
            else:
                buffer:int = prev_y_index

        font_size:int = 11 # __detect_font_size(current_line, debug=debug)
        last_font_size:int = font_size if last_result_line is None else last_result_line.font_size

        if font_size != last_font_size and buffer == prev_y_index:
            buffer += 1

        current_y_index:int = buffer
        current_x_index:int = current_coords[0]

        word:str = current_line.word
        translation:str = current_line.translation
        align:alignment = __detect_alignment(current_coords, debug=debug)

        to_append:layout_row = layout_row(
            word=word,
            translation=translation, 
            document_column=current_x_index,
            document_row=current_y_index,            
            font_size=font_size,
            alignment=str(align)
        )

        result_tmp.append(to_append)

    result_tmp.sort(key=lambda x: (x.document_column, x.document_row))

    return result_tmp

def __order(input:list[layout_row]) -> list[layout_row]:    
    return sorted(input, key=lambda x: (x.document_row, x.document_row))

def coordinates_to_lines(input, debug: bool = False) -> list[layout_row]:
    sorted_input:list[row] = __prepare_for_processing(input, debug)
    result_tmp:list[layout_row] = __create_layout(sorted_input, debug)
    result:list[layout_row] = __order(result_tmp)

    if debug:
        print('\n========================================\n')

        for line in sorted_input:
            print(line)

        print()

        for line in result:
            print(line)

        print()
        print("Input length:", len(input))
        print("Sorted length:", len(sorted_input))
        print("Result length:", len(result))

    return result

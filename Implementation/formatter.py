from __future__ import annotations
from collections import defaultdict

class alignment:
    def __init__(self, kind:str):
        self.__VALID_ALIGNMENTS:list[str] = ['L', 'C', 'R']

        if kind not in self.__VALID_ALIGNMENTS:
            raise ValueError(f"Invalid alignment >> {kind} <<. Must be from {self.__VALID_ALIGNMENTS}")
        
        self.kind:str = kind

    def __eq__(self, what:(alignment | str)) -> bool:
        if what is None:
            return False
        
        if isinstance(what, str):
            for character in self.__VALID_ALIGNMENTS:
                if character == what and character == self.kind:
                    return True
        elif isinstance(what, alignment):
            for character in self.__VALID_ALIGNMENTS:
                if character == what.kind and character == self.kind:
                    return True
        else:
            return False
        
    def __str__(self) -> str:
        return self.kind


def __fibonacci(n:int) -> int:
    n += 5
    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a - 2

def __linear(n:int) -> int:
    n += 3
    return 2 * n

def __detect_font_size(rect:list[int], func=__fibonacci, debug:bool=False) -> int:
    y_min:int = rect[2]
    y_max:int = rect[3]
    diff:int = abs(y_max - y_min)
    bucket:int = int((diff) / 10)
    result:int = func(bucket)

    if debug:
        print(f'Wykryto rozmiar czcionki między [{y_min}, {y_max}]: {diff}, {bucket}, rozmiar: {result}')

    return result

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

def __prepare_for_processing(input_data, debug:bool = False):
    sorted_input = []

    for line in input_data:
        coords_raw = line[1]
        x_1, y_1 = coords_raw[0]
        x_2, y_2 = coords_raw[1]
        x_3, y_3 = coords_raw[2]
        x_4, y_4 = coords_raw[3]

        x_min = min(x_1, x_4)
        x_max = max(x_2, x_3)
        y_min = min(y_1, y_2)
        y_max = max(y_3, y_4)

        coords_list = [int(x_min), int(x_max), int(y_min), int(y_max)]
        sorted_input.append([coords_list, line[0], line[2]])

    sorted_input.sort(key=lambda x: (x[0][2], x[0][0]))

    return sorted_input

def __create_layout(sorted_input, debug: bool = False):
    result_tmp = []
    last_line = None
    line_changed:bool = False

    for index, current_line in enumerate(sorted_input):
        if index == 1:
            last_line = sorted_input[0]
        elif line_changed and index > 1:
            last_line = sorted_input[index - 1]
            line_changed = False

        last_result_line = result_tmp[index - 1] if result_tmp else None
        prev_y_index = 0 if last_result_line is None else last_result_line[2][0]
        current_coords = current_line[0]
        buffer:int = 0

        if last_line is not None:            
            last_coords = last_line[0]

            cur_y_min = current_coords[2]
            last_y_max = last_coords[3]

            if cur_y_min >= last_y_max:
                buffer = prev_y_index + 1
                line_changed = True
            else:
                buffer = prev_y_index

        font_size:int = __detect_font_size(current_coords, debug=debug)
        last_font_size:int = font_size if last_result_line is None else last_result_line[2][2]

        if font_size != last_font_size and buffer == prev_y_index:
            buffer += 1

        current_y_index:int = buffer
        current_x_index:int = current_coords[0]

        word:str = current_line[1]
        translation:str = current_line[2]
        align:alignment = __detect_alignment(current_coords, debug=debug)

        to_append = [word, translation, (current_y_index, current_x_index, font_size, str(align))]
        result_tmp.append(to_append)

    result_tmp.sort(key=lambda x: (x[2][0], x[2][1]))

    return result_tmp

def __order(result_tmp):
    result = []
    groups = defaultdict(list)

    for item in result_tmp:
        line, pos, _, _ = item[2]
        groups[line].append((pos, item))

    for line in sorted(groups):
        sorted_items = sorted(groups[line], key=lambda x: x[0])

        for new_index, (_, item) in enumerate(sorted_items):
            line, _, size, align = item[2]
            new_item = [item[0], item[1], (line, new_index, size, align)]
            result.append(new_item)

    return result

def coordinates_to_lines(input, debug: bool = False):
    sorted_input = __prepare_for_processing(input, debug)
    result_tmp = __create_layout(sorted_input, debug)
    result = __order(result_tmp)

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

def format_for_translation(input: (list[tuple[list, str]] | list[list[list | str]]), debug:bool=False) -> list[list[list | str]]:
    result:list[list[list | str]] = []
    
    for line in input:
        result.append(list(line))

    return result

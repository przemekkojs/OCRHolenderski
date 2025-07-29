def format_for_translation(input: (list[tuple[list, str]] | list[list[list | str]]), debug:bool=False) -> list[list[list | str]]:
    result:list[list[list | str]] = []
    
    for line in input:
        result.append(list(line))

    return result

def __detect_font_size(debug:bool=False) -> int:
    return 14

# word, word_translated, (line, column, font_size)
def coordinates_to_lines(input: (list[tuple[list, str, str]] | list[list[list | str]]), debug:bool=False) -> list[list[str | str | tuple[int, int, int]]]:
    sorted_input:list[list[list | str]] = []
    result:list[list[str | str | tuple[int, int, int]]] = []

    for line in input:
        coords_raw:list = line[1]
        x_1:int = coords_raw[0][0]
        y_1:int = coords_raw[0][1]
        x_2:int = coords_raw[1][0]
        y_2:int = coords_raw[1][1]
        x_3:int = coords_raw[2][0]
        y_3:int = coords_raw[2][1]
        x_4:int = coords_raw[3][0]
        y_4:int = coords_raw[3][1]

        x_min:int = min(x_1, x_4)
        x_max:int = max(x_2, x_3)
        y_min:int = min(y_1, y_2)
        y_max:int = max(y_3, y_4)

        coords_list:list[int] = [int(x_min), int(x_max), int(y_min), int(y_max)]
        sorted_input.append([coords_list, line[0], line[2]])

    sorted_input.sort(key=lambda x: (x[0][2], x[0][0]))

    last_line:(list[list | str] | None) = None
    line_changed:bool = False

    for index in range(len(sorted_input)):
        if index == 1:
            last_line = sorted_input[0]
        elif line_changed and index > 1:
            last_line = sorted_input[index - 1]
            line_changed = False

        current_line:list[list | str] = sorted_input[index]        
        last_result_line:(list[str | str | tuple[int, int, int]] | None) = result[index - 1] if len(result) > 0 else None
        
        if debug:
            print(current_line)

        prev_y_index:int = 0 if last_result_line == None else last_result_line[2][0]
        buffer:int = 0

        if last_line != None:
            current_coords:list[int] = current_line[0]
            last_coords:list[int] = last_line[0]

            cur_y_min:int = current_coords[2]
            last_y_max:int = last_coords[3]

            if cur_y_min >= last_y_max:
                buffer = prev_y_index + 1
                line_changed = True
            else:
                buffer = prev_y_index
        
        current_y_index:int = buffer
        current_x_index:int = sorted_input[index][0][0] #0 if (prev_y_index != current_y_index or last_result_line == None) else (last_result_line[2][1] + 1)
        font_size:int = __detect_font_size(debug)
        word:str = current_line[1]
        translation:str = current_line[2]
        to_append:list[str | str | tuple[int, int, int]] = [word, translation, (current_y_index, current_x_index, font_size)]
        result.append(to_append)

    result.sort(key=lambda x: (x[2][0], x[2][1]))

    if debug:
        print('\n========================================\n')

        for line in sorted_input:
            print(line)

        print()

        for line in result:
            print(line)

        print()
        print("Input length", len(input))
        print("Sorted length", len(sorted_input))
        print("Result length", len(result))

    return result

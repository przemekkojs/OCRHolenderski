from collections import defaultdict

# TODO
def __detect_font_size(debug:bool=False) -> int:
    return 14

def __prepare_for_processing(input_data, debug: bool = False):
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
    line_changed = False

    for index, current_line in enumerate(sorted_input):
        if index == 1:
            last_line = sorted_input[0]
        elif line_changed and index > 1:
            last_line = sorted_input[index - 1]
            line_changed = False

        last_result_line = result_tmp[index - 1] if result_tmp else None
        prev_y_index = 0 if last_result_line is None else last_result_line[2][0]
        buffer = 0

        if last_line is not None:
            current_coords = current_line[0]
            last_coords = last_line[0]

            cur_y_min = current_coords[2]
            last_y_max = last_coords[3]

            if cur_y_min >= last_y_max:
                buffer = prev_y_index + 1
                line_changed = True
            else:
                buffer = prev_y_index

        font_size = __detect_font_size(debug)
        current_y_index = buffer
        current_x_index = current_line[0][0]

        word = current_line[1]
        translation = current_line[2]

        to_append = [word, translation, (current_y_index, current_x_index, font_size)]
        result_tmp.append(to_append)

    result_tmp.sort(key=lambda x: (x[2][0], x[2][1]))

    return result_tmp

def __order(result_tmp):
    result = []
    groups = defaultdict(list)

    for item in result_tmp:
        line, pos, size = item[2]
        groups[line].append((pos, item))

    for line in sorted(groups):
        sorted_items = sorted(groups[line], key=lambda x: x[0])

        for new_index, (_, item) in enumerate(sorted_items):
            line, _, size = item[2]
            new_item = [item[0], item[1], (line, new_index, size)]
            result.append(new_item)

    return result

# word, word_translated, (line, column, font_size)
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

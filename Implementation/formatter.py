def format_for_translation(input: (list[tuple[list, str]] | list[list[list, str]])) -> dict[str, list[list, str]]:        
    result:dict[str, list[list, str]] = {}
    
    for tpl in input:
        points:list = tpl[0]
        word:str = tpl[1]

        result[word] = [points, ""]

    return result

def format_for_translation(input: list[tuple[list, str]]) -> dict[str, tuple[list, str]]:
    if not isinstance(input, (list[tuple[list, str]], list[list[list, str]])):
        raise ValueError("Invalid variable type")
    
    
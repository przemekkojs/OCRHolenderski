SUPPORTED_LANGUAGES:list[str] = [
    'nl'
]

CODES_TO_MODEL_CODES:dict[str, str] = {
    'nl' : 'nld_Latn',
    'pl' : 'pol_Latn'
}

def check_if_language_exists(language:str) -> bool:
    return language in SUPPORTED_LANGUAGES

# TODO
def language_code_to_adjective(code:str, lang:str='pl') -> str:
    return "niderlandzkiego"

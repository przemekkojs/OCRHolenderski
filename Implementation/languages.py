SUPPORTED_LANGUAGES = [
    'nl'
]

def check_if_language_exists(language:str) -> bool:
    return language in SUPPORTED_LANGUAGES

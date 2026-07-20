import unicodedata

def remove_accents(value: str):
    return "".join(
        c
        for c in unicodedata.normalize("NFD", value)
        if unicodedata.category(c) != "Mn"
    )


def normalize(value: str):

    if not value:
        return ""
    
    value = value.strip()
    value = value.lower()
    value = remove_accents(value)
    return value
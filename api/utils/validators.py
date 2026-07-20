def is_registration(value: str):
    return value.isdigit()


def is_empty(value):
    return not value or not value.strip()
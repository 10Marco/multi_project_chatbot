import html

def text(value):

    if value is None:
        return ""
    value = value.strip()
    value = html.escape(value)
    return value
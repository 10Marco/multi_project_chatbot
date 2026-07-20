import re

def digits(phone: str) -> str:
    return re.sub(r"\D", "", phone)

def remove_whatsapp_suffix(phone: str) -> str:
    return phone.split("@")[0]

def normalize(phone):
    if not phone:
        return ""
    return digits(
        remove_whatsapp_suffix(phone)
    )
from services.glpi.models.reply import Reply


def build(title, options, formatter):

    text = f"{title}\n\n"

    for index, option in enumerate(options, start=1):
        text += f"{index}. {formatter(option)}\n"

    return Reply.text(text)


def resolve(message, options):

    if not message.isdigit():
        return None

    index = int(message) - 1

    if index < 0 or index >= len(options):
        return None

    return options[index]
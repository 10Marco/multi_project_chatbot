from dataclasses import dataclass, field


@dataclass
class Reply:

    type: str

    data: dict = field(default_factory=dict)

    @classmethod
    def text(cls, text: str):

        return cls(
            type="text",
            data={
                "text": text
            }

        )

    @classmethod
    def image(cls, url: str):

        return cls(
            type="image",
            data={
                "url": url
            }
        )

    @classmethod
    def document(cls, url: str, filename: str):

        return cls(
            type="document",
            data={
                "url": url,
                "filename": filename
            }

        )

    @classmethod
    def buttons(cls, text: str, buttons: list):

        return cls(
            type="buttons",
            data={
                "text": text,
                "buttons": buttons
            }

        )

    @classmethod
    def list(cls, text: str, sections: list):

        return cls(
            type="list",
            data={
                "text": text,
                "sections": sections
            }
        )
from dataclasses import dataclass, field
from services.glpi.models.base_model import BaseModel

@dataclass
class Reply(BaseModel):

    type: str
    data: dict = field(default_factory=dict)

    @classmethod
    def text(cls, text):
        return cls(
            type="text",
            data={
                "text": text
            }
        )

    @classmethod
    def image(cls, image, caption=None):
        return cls(
            type="image",
            data={
                "image": image,
                "caption": caption
            }
        )

    @classmethod
    def document(cls, document, filename, caption=None):
        return cls(
            type="document",
            data={
                "document": document,
                "filename": filename,
                "caption": caption
            }
        )

    @classmethod
    def buttons(cls, text, buttons):
        return cls(
            type="buttons",
            data={
                "text": text,
                "buttons": buttons
            }
        )

    @classmethod
    def list(cls, title, options):
        return cls(
            type="list",
            data={
                "title": title,
                "options": options
            }
        )

    @classmethod
    def action(cls, action, data=None):
        return cls(
            type="action",
            data={
                "action": action,
                "data": data or {}
            }
        )    
        
    
    @classmethod
    def success(cls, text):
        return cls.text(f"✅ {text}")

    @classmethod
    def error(cls, text):
        return cls.text(f"❌ {text}")

    @classmethod
    def warning(cls, text):
        return cls.text(f"⚠️ {text}")

    @classmethod
    def info(cls, text):
        return cls.text(f"ℹ️ {text}")
    
    @classmethod
    def sifop_folha(cls, tipo, id, mes, filename):
        return cls(
            type="sifop_folha",
            data={
                "tipo": tipo,
                "id": id,
                "mes": mes,
                "filename": filename
            }
        )
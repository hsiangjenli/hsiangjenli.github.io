from pydantic import BaseModel, AnyHttpUrl
from enum import Enum

class FontAwesomeIcon(Enum):
    HOME = "home"
    USER = "user"
    CART = "cart"
    PDF = "file-pdf"
    WEB = "globe"
    MAIL = "envelope"
    IMAGE = "image"
    GOOGLE_DRIVE = "google-drive"
    LINK = "link"

class HtmlIcon(BaseModel):
    text: str
    fontawesom: str
    href: AnyHttpUrl

    EXTENSION_MAPPING = {
        (".pdf",): FontAwesomeIcon.PDF,
        (".png", ".jpg", ".jpeg", ".gif", ".bmp"): FontAwesomeIcon.IMAGE,
    }

    DOMAIN_MAPPING = {
        "drive.google.com": FontAwesomeIcon.GOOGLE_DRIVE,
    }

    @property
    def icon_type(self) -> FontAwesomeIcon:

        if not self.href:
            return FontAwesomeIcon.UNKNOWN

        url = self.href.lower()

        for extensions, icon in self.EXTENSION_MAPPING.items():
            if url.endswith(extensions):
                return icon

        for domain, icon in self.DOMAIN_MAPPING.items():
            if domain in url:
                return icon

        return FontAwesomeIcon.LINK

    @property
    def html(self) -> str:
        if self.fontawesom:
            icon_html = f'<i class="{self.fontawesom}"></i>'
        else:
            icon_html = f'<i class="{self.icon_type.value}"></i>'
        if self.href:
            return f'<a href="{self.href}" target="_blank">{icon_html}</a>'
        return icon_html
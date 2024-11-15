from enum import Enum
from typing import ClassVar

from pydantic import AnyHttpUrl, BaseModel


class FontAwesomeIcon(Enum):
    PDF = "fa-solid fa-file-pdf"
    WEB = "fa-solid fa-globe"
    MAIL = "fa-solid fa-envelope"
    IMAGE = "fa-solid fa-image"
    GOOGLE_DRIVE = "fa-brands fa-google-drive"
    GITHUB = "fa-brands fa-github"
    DEFAULT = "fa-solid fa-link"


class HtmlIcon(BaseModel):
    text: str
    fontawesom: str = None
    href: AnyHttpUrl

    EXTENSION_MAPPING: ClassVar[dict[tuple[str, ...], FontAwesomeIcon]] = {
        (".pdf",): FontAwesomeIcon.PDF,
        (".png", ".jpg", ".jpeg", ".gif", ".bmp"): FontAwesomeIcon.IMAGE,
    }

    DOMAIN_MAPPING: ClassVar[dict[str, FontAwesomeIcon]] = {
        "drive.google.com": FontAwesomeIcon.GOOGLE_DRIVE,
        "github.com": FontAwesomeIcon.GITHUB,
    }

    @property
    def icon_type(self) -> FontAwesomeIcon:
        if not self.href:
            return FontAwesomeIcon.DEFAULT

        url = str(self.href).lower()
        for extensions, icon in self.EXTENSION_MAPPING.items():
            if url.endswith(extensions):
                return icon

        for domain, icon in self.DOMAIN_MAPPING.items():
            if domain in url:
                return icon

        return FontAwesomeIcon.LINK

    @property
    def html(self) -> str:
        icon_html = f'<i class="{self.icon_type.value}"></i>'
        if self.href:
            return (
                f'<a href="{self.href}" target="_blank"> {icon_html} {self.text} </a>'
            )
        return icon_html


if __name__ == "__main__":
    icon = HtmlIcon(text="PDF", href="https://example.com/document.pdf")
    print(icon.html)

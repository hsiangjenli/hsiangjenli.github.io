from enum import Enum
from typing import ClassVar
import datetime
from typing import Optional
from pathlib import Path

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

class EntryInfo(BaseModel):

    period_start: Optional[datetime.date]
    period_end: Optional[datetime.date]

    resource: Optional[list[HtmlIcon]]

    tags: Optional[list[str]]

class EntryDescription(BaseModel):
    title: str
    description: Optional[list[str]]

class Entry(BaseModel):
    info: EntryInfo
    english: EntryDescription
    chinese: EntryDescription

class TomlFile(BaseModel):
    entries: list[Entry]

    @classmethod
    def load(cls, path: Path) -> list[Entry]:
        data = toml.load(path)
        return cls(entries=[data[entry] for entry in data])

if __name__ == "__main__":
    import toml

    data = TomlFile.load("config/test.toml")

    print(data)
    # data = toml.load("config/test.toml")

    # # data = TomlFile.load("config/test.toml")
    # print(data['awesomeLLM'])
    # # info = EntryInfo(**data["awesomeLLM"]['info'])
    # # print(info)
    # entry = Entry(**data['awesomeLLM'])
    # print(entry)
    # icon = HtmlIcon(text="PDF", href="https://example.com/document.pdf")
    # print(icon.html)

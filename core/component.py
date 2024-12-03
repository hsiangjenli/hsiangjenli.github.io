import datetime
from enum import Enum
from pathlib import Path
from typing import ClassVar, Optional, Union

import toml
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator


class FontAwesomeIcon(Enum):
    PDF = "fa-solid fa-file-pdf"
    WEB = "fa-solid fa-globe"
    MAIL = "fa-solid fa-envelope"
    IMAGE = "fa-solid fa-image"
    GOOGLE_DRIVE = "fa-brands fa-google-drive"
    GITHUB = "fa-brands fa-github"
    DEFAULT = "fa-solid fa-link"


class HtmlIcon(BaseModel):
    text: str = None
    fontawesome: str = None
    href: AnyHttpUrl = None

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

        return FontAwesomeIcon.DEFAULT

    @property
    def style(self) -> str:
        return "min-width: 40px; text-align: center;"

    @property
    def html(self) -> str:
        icon_html = f'<i style="{self.style}" class="{self.icon_type.value}"></i>'
        if self.href:
            return f'<a href="{self.href}" style="font-weight: bold" target="_blank"> {icon_html}{self.text} </a>'
        return icon_html

    @property
    def icon(self) -> str:
        icon_html = f'<i style="{self.style}" class="{self.icon_type.value}"></i>'
        if self.fontawesome:
            return f'<i style="{self.style}" class="{self.fontawesome}"></i>'
        if not self.href:
            return icon_html
        return f'<a href="{self.href}" style="font-weight: bold;" target="_blank"> {icon_html} </a>'


class EntryInfo(BaseModel):
    period_start: Optional[Union[datetime.date, str]] = Field("Now")
    period_end: Optional[Union[datetime.date, str]] = Field("Now", alias="graduation")

    resource: Optional[list[HtmlIcon]] = None

    tags: Optional[list[str]] = None
    weight: Optional[int] = 0
    image: HtmlIcon = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @field_validator("period_start", "period_end")
    def parse_date(cls, value):
        if isinstance(value, str):
            return value
        # 處理多種時間格式
        formats = ["%Y-%m-%d", "%Y.%m", "%Y"]
        for fmt in formats:
            try:
                return datetime.datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Invalid date format: {value}")

    @property
    def period_start_year(self):
        if isinstance(self.period_start, datetime.date):
            return self.period_start.year
        return self.period_start

    @property
    def period_end_year(self):
        if isinstance(self.period_end, datetime.date):
            return self.period_end.year
        return self.period_end

    @property
    def period_start_year_month(self):
        if isinstance(self.period_start, datetime.date):
            return self.period_start.strftime("%Y-%m")
        return self.period_start

    @property
    def period_end_year_month(self):
        if isinstance(self.period_end, datetime.date):
            return self.period_end.strftime("%Y-%m")
        return self.period_end


class EntryDescription(BaseModel):
    title: str = Field(alias="university")
    description: Optional[list[str]] = []
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @property
    def university(self):
        return self.title


class Entry(BaseModel):
    info: EntryInfo
    english: EntryDescription
    chinese: EntryDescription
    model_config = ConfigDict(extra="allow")


class TomlFile(BaseModel):
    entries: list[Entry]

    @classmethod
    def load(cls, path: Path) -> list[Entry]:
        data = toml.load(path)
        return cls(entries=[data[entry] for entry in data])


class SkillTomlFile(BaseModel):
    entries: dict[str, list[Entry]]  # 動態解析各分類

    @classmethod
    def load(cls, path: str):
        data = toml.load(path)
        return cls(
            entries={
                entry: [data[entry][skill] for skill in data[entry]] for entry in data
            }
        )


if __name__ == "__main__":
    import toml

    data = TomlFile.load("config/test.toml")

    for entry in data.entries:
        for r in entry.info.resource:
            print(r.html)

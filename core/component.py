import datetime
from enum import Enum
from pathlib import Path
from typing import ClassVar, Optional, Union

import toml
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator


def _parse_period_value(
    value: datetime.date | str, *, is_end: bool
) -> tuple[int, int, int]:
    if isinstance(value, datetime.date):
        return (value.year, value.month, value.day)

    normalized = value.strip().lower()
    if normalized == "now":
        return (9999, 12, 31) if is_end else (0, 1, 1)

    for fmt in ("%Y-%m-%d", "%Y.%m", "%Y"):
        try:
            parsed = datetime.datetime.strptime(value, fmt).date()
            return (parsed.year, parsed.month, parsed.day)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {value}")


def _common_prefix(values: list[str]) -> str:
    if not values:
        return ""

    prefix = values[0]
    for value in values[1:]:
        while prefix and not value.startswith(prefix):
            prefix = prefix[:-1]

    prefix = prefix.rstrip(" -_/")
    if not prefix:
        return values[0]

    if " " in prefix and prefix != values[0]:
        prefix = prefix.rsplit(" ", 1)[0].rstrip(" -_/") or prefix
    return prefix


def _month_index(value: datetime.date | str, *, is_end: bool) -> int:
    year, month, _ = _parse_period_value(value, is_end=is_end)
    return year * 12 + month


class RepoStatus(Enum):
    ACTIVE = "active"
    DONE = "done"
    ARCHIVED = "archived"


class FontAwesomeIcon(Enum):
    PDF = "fa-solid fa-file-pdf"
    WEB = "fa-solid fa-globe"
    MAIL = "fa-solid fa-envelope"
    IMAGE = "fa-solid fa-image"
    GOOGLE_DRIVE = "fa-brands fa-google-drive"
    GITHUB = "fa-brands fa-github"
    OVERLEAF = "fa-solid fa-superscript"
    SCHOOL = "fa-solid fa-school"
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
        "overleaf.com": FontAwesomeIcon.OVERLEAF,
        "edu.tw": FontAwesomeIcon.SCHOOL,
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
        return "min-width: 25px; text-align: left;"

    @property
    def html(self) -> str:
        if self.fontawesome:
            icon_html = f'<i style="{self.style}" class="{self.fontawesome}"></i>'
        else:
            icon_html = f'<i style="{self.style}" class="{self.icon_type.value}"></i>'

        if self.href and self.fontawesome:
            return f'<a href="{self.href}" style="font-weight: bold" target="_blank"> {icon_html}{self.text} </a>'
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
    status: Optional[RepoStatus] = RepoStatus.DONE
    group: Optional[str] = None

    resource: Optional[list[HtmlIcon]] = []

    tags: Optional[list[str]] = []
    weight: Optional[int] = 0
    image: HtmlIcon = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @field_validator("status")
    def check_status(cls, value):
        if value is None:
            return RepoStatus.DONE
        if isinstance(value, str):
            value = value.lower()
            if value == "active":
                return RepoStatus.ACTIVE
            elif value == "archived":
                return RepoStatus.ARCHIVED
            else:
                raise ValueError(f"Invalid status: {value}")

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

    @property
    def period_end_year_month_equal_now(self):
        if self.period_end.lower() == "now":
            return "Now 🔥🔥🔥"
        return self.period_end_year_month


class EntryDescription(BaseModel):
    title: str = Field(alias="university")
    group_title: Optional[str] = None
    description: Optional[list[str]] = []
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @property
    def university(self):
        return self.title

    @field_validator("description", mode="before")
    def capitalize_first_letter(cls, description):
        return [d.capitalize() for d in description]


class Entry(BaseModel):
    entry_id: str = Field(default="", exclude=True)
    info: EntryInfo
    english: EntryDescription
    chinese: EntryDescription
    model_config = ConfigDict(extra="allow")

    @property
    def group_key(self) -> str:
        if self.info.group:
            return self.info.group
        if not self.entry_id:
            return self.english.title.lower()
        return self.entry_id.split("_", 1)[0]


class EntryGroup(BaseModel):
    entries: list[Entry]

    def _custom_group_title(self, language: str) -> str | None:
        for entry in self.entries:
            description = getattr(entry, language)
            if description.group_title:
                return description.group_title
        return None

    def can_merge(self, entry: Entry) -> bool:
        last_entry = self.entries[-1]

        if last_entry.group_key != entry.group_key:
            return False

        newer_start = _month_index(last_entry.info.period_start, is_end=False)
        older_end = _month_index(entry.info.period_end, is_end=True)
        return older_end + 1 >= newer_start

    @property
    def english_title(self) -> str:
        custom_title = self._custom_group_title("english")
        if custom_title:
            return custom_title
        if len(self.entries) == 1:
            return self.entries[0].english.title
        return _common_prefix([entry.english.title for entry in self.entries])

    @property
    def chinese_title(self) -> str:
        custom_title = self._custom_group_title("chinese")
        if custom_title:
            return custom_title
        if len(self.entries) == 1:
            return self.entries[0].chinese.title
        return _common_prefix([entry.chinese.title for entry in self.entries])

    @property
    def period_start_year_month(self) -> str:
        entry = min(
            self.entries,
            key=lambda candidate: _parse_period_value(
                candidate.info.period_start, is_end=False
            ),
        )
        return entry.info.period_start_year_month

    @property
    def period_end_year_month(self) -> str:
        entry = max(
            self.entries,
            key=lambda candidate: _parse_period_value(
                candidate.info.period_end, is_end=True
            ),
        )
        return entry.info.period_end_year_month

    @property
    def show_entry_title(self) -> bool:
        return any(entry.english.title != self.english_title for entry in self.entries)


class TomlFile(BaseModel):
    entries: list[Entry]

    @classmethod
    def load(cls, path: Path) -> list[Entry]:
        data = toml.load(path)
        return cls(entries=[Entry(entry_id=entry, **data[entry]) for entry in data])

    @property
    def grouped_entries(self) -> list[EntryGroup]:
        grouped_entries: list[EntryGroup] = []

        for entry in self.entries:
            if grouped_entries and grouped_entries[-1].can_merge(entry):
                grouped_entries[-1].entries.append(entry)
                continue
            grouped_entries.append(EntryGroup(entries=[entry]))

        return grouped_entries


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

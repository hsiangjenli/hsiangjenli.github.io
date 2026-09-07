"""Load site-level configuration."""

from dataclasses import dataclass
from pathlib import Path

import toml


@dataclass(frozen=True)
class SiteSettings:
    """Configuration shared by all generated locale pages."""

    site: dict
    author: dict
    ui: dict[str, dict]

    @classmethod
    def load(cls, path: Path) -> "SiteSettings":
        """Load and minimally validate a site TOML document."""
        document = toml.load(path)
        for key in ("site", "author", "ui"):
            if key not in document:
                raise ValueError(f"site configuration is missing [{key}]")
        return cls(site=document["site"], author=document["author"], ui=document["ui"])

    @property
    def locales(self) -> tuple[str, ...]:
        """Return configured locale keys in TOML order."""
        return tuple(self.ui)

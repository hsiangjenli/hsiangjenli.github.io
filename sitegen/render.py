"""Build locale-aware Jinja contexts and render output files."""

import shutil
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from sitegen.blog import latest_posts
from sitegen.data import ResumeData
from sitegen.settings import SiteSettings


def build_site(root: Path, output_dir: Path, settings: SiteSettings, data: ResumeData, dev_mode: bool) -> None:
    """Render every locale and copy static assets to an isolated output folder."""
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    shutil.copytree(root / "static", output_dir / "static")
    environment = Environment(
        loader=FileSystemLoader(root / "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = environment.get_template("resume/base.html")
    for locale in settings.locales:
        target = output_dir if locale == settings.site["default_locale"] else output_dir / locale
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(template.render(**build_context(settings, data, locale, dev_mode)), encoding="utf-8")


def build_context(settings: SiteSettings, data: ResumeData, locale: str, dev_mode: bool) -> dict:
    """Create one template context without duplicating bilingual data files."""
    language_key = "english" if locale == "en" else "chinese"
    alternate_locale = next(item for item in settings.locales if item != locale)
    return {
        "site": settings.site,
        "author": settings.author,
        "ui": settings.ui[locale],
        "locale": locale,
        "language_key": language_key,
        "alternate_url": "/" if locale != "en" else f"/{alternate_locale}/",
        "asset_prefix": "" if locale == settings.site["default_locale"] else "../",
        "last_updated": datetime.now(timezone.utc).date().isoformat(),
        "copyright_year": datetime.now(timezone.utc).year,
        "dev_mode": dev_mode,
        "education": data.education,
        "experience_groups": data.experience_groups,
        "skills": data.skills,
        "awards": data.awards,
        "projects": data.projects,
        "pull_requests": data.pull_requests,
        "blog_posts": latest_posts(settings.site["blog_api_url"], locale),
    }

from pathlib import Path

from sitegen.data import load_resume_data
from sitegen.render import build_site
from sitegen.settings import SiteSettings

ROOT = Path(__file__).parents[1]


def test_site_configuration_and_bilingual_render(tmp_path: Path) -> None:
    settings = SiteSettings.load(ROOT / "config" / "site.toml")
    data = load_resume_data(ROOT / "config")
    build_site(ROOT, tmp_path, settings, data, dev_mode=True)
    assert (tmp_path / "index.html").is_file()
    assert (tmp_path / "zh-TW" / "index.html").is_file()
    assert "Hsiang-Jen Li" in (tmp_path / "index.html").read_text()
    assert "學歷" in (tmp_path / "zh-TW" / "index.html").read_text()

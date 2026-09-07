"""Command-line entry point for rendering the bilingual resume site."""

import argparse
from pathlib import Path

from sitegen.data import load_resume_data
from sitegen.render import build_site
from sitegen.settings import SiteSettings


def main() -> None:
    """Render English and Traditional Chinese pages into the output directory."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", help="Disable analytics in output.")
    parser.add_argument("--output", default="dist", help="Generated-site directory.")
    arguments = parser.parse_args()
    root = Path(__file__).parent.resolve()
    settings = SiteSettings.load(root / "config" / "site.toml")
    data = load_resume_data(root / "config")
    build_site(root, root / arguments.output, settings, data, arguments.dev)


if __name__ == "__main__":
    main()

from pathlib import Path

import toml
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, Template


def html_formater(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    pretty_soup = soup.prettify()
    return pretty_soup


def load_toml(path: str | Path):
    with open(path, "r") as f:
        return toml.load(f)


def set_environemnt(folder: str | Path, template: str) -> Template:
    env = Environment(
        loader=FileSystemLoader(folder),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
    )
    rendered_template = env.get_template(template)
    return rendered_template


def latex_set_environemnt(folder: str | Path, template: str) -> Template:
    env = Environment(
        block_start_string="<<%",
        block_end_string="%>>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<<#",
        comment_end_string="#>>",
        trim_blocks=True,
        lstrip_blocks=True,
        loader=FileSystemLoader(folder),
    )
    rendered_template = env.get_template(template)
    return rendered_template


def write(string: str, output: str | Path) -> None:
    with open(output, "w", encoding="utf-8") as f:
        f.write(string)

from jinja2 import Environment, FileSystemLoader
import toml
from bs4 import BeautifulSoup

def html_formater(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    pretty_soup = soup.prettify()
    return pretty_soup

def load_toml(path: str):    
    with open(path, "r") as f:
        return toml.load(f)

def set_environemnt(folder: str, template: str):
    env = Environment(loader=FileSystemLoader(folder))
    template = env.get_template(template)
    return template

def latex_set_environemnt(folder: str, template: str):
    env = Environment(
        block_start_string='<<%',
        block_end_string='%>>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<<#',
        comment_end_string='#>>',
        loader=FileSystemLoader(folder),
    )
    template = env.get_template(template)
    return template

def write(string, output):
    with open(output, 'w', encoding='utf-8') as f:
        f.write(string)
from jinja2 import Environment, FileSystemLoader
import toml

def load_toml(path: str):    
    with open(path, "r") as f:
        return toml.load(f)

def set_environemnt(folder: str, template: str):
    env = Environment(loader=FileSystemLoader(folder))
    template = env.get_template(template)
    return template

def write(string, output):
    with open(output, 'w', encoding='utf-8') as f:
        f.write(string)
import os
import shutil
import requests
import datetime
import argparse
from core import tutils

# == personal information ============================================================================================
Q = "<div>The way lead to success is your own resolution.</div><div>得常咬菜根，即做百事成。</div>"

NAME = "Hsiang-Jen Li"
ZH_TW_NAME = "李享紝"
NICKNAME = "RN"

SEEKING_POSITION = [
    "Seeking a Data & MLOps Engineer role with a focus on research and complex data relationships",
    "Learning best through teaching, I write IT blogs and encourage others to share knowledge, promoting shared growth and learning",
    "Establishing and enforcing development standards: Skilled in creating clear and comprehensive development rules, ensuring developers maintain consistency in variable naming, commit messages, and other practices to avoid disorganization and maintain project quality",
    "Code standards and documentation automation: Proficient in adhering to PEP8 and other Python coding standards, using tools to maintain code quality, and following Python docstring conventions for efficient documentation generation. Capable of using local language models to automatically generate compliant commit messages, improving team communication and project transparency",
    "Unified development, version control, and deployment environments: Expertise in Git, utilizing branches and tags to distinguish WIP, development, and production-ready projects. Proficient in setting up custom GitHub Workflows to automate processes, such as triggering project releases upon push tags. Also experienced in using Docker to create consistent development and deployment environments, ensuring stability and consistency between development and production environments"
    ]
CURRENT_POSITION = "Finance & CS Background | Data Analyst @ SCSB"

GITHUB = "hsiangjenli"
MAIL = "hsiangjenli@gmail.com"
IT_BLOG = "https://hsiangjenli.github.io/blog/"
CHEATSHEET = "https://hsiangjenli.github.io/cheat-sheet/"

EDU = tutils.load_toml("config/_education.toml")
EXP = tutils.load_toml("config/_experience.toml")
SKILL = tutils.load_toml("config/_skill.toml")
RI = tutils.load_toml("config/_research.toml")
SIDE_PROJECT = tutils.load_toml("config/_project.toml")
PULL_REQUEST = tutils.load_toml("config/_open_source.toml")
AWARD = tutils.load_toml("config/_award.toml")
BLOG_POST = requests.get("https://hsiangjenli.github.io/blog/api/getPosts/").json()['data']['posts']
BLOG_POST = sorted(BLOG_POST, key=lambda x: x['date'], reverse=True)

# == webpage ==========================================================================================================
WEBPAGE = "hsiangjenli.github.io"
WEBPAGE_TEMPLATE = tutils.set_environemnt(folder='static/template/html/read_only', template='index.html')

# == CV ==============================================================================================================
CV_ENG_TEMPLATE = tutils.set_environemnt(folder='static/template/html/cv_eng', template='index.html')

# == latex ===========================================================================================================
LATEX_TEMPLATE = tutils.latex_set_environemnt(folder='static/template/latex', template='resume.tex')

# == main ============================================================================================================
if __name__ == "__main__":

    args = argparse.ArgumentParser()
    args.add_argument("--dev", help="Development mode", default=False, type=bool)
    args = args.parse_args()

    if args.dev:
        DEV = bool(args.dev)
    
    shutil.rmtree(f"{WEBPAGE}/static", ignore_errors=True)
    os.makedirs(f"{WEBPAGE}/static", exist_ok=True)

    LAST_UPDATE = datetime.datetime.now().strftime("%Y-%m-%d")
    YEAR = f"2024 ~ {datetime.datetime.now().year}" if datetime.datetime.now().year > 2024 else 2024
    COPYRIGHT = f"© {YEAR} Hsiang-Jen Li. All rights reserved."

    PERSONAL_INFO = {
        "Q": Q,
        "NAME": NAME,
        "ZH_TW_NAME": ZH_TW_NAME, 
        "NICKNAME": NICKNAME,
        "SEEKING_POSITION": SEEKING_POSITION,
        "CURRENT_POSITION": CURRENT_POSITION,
        "GITHUB": GITHUB,
        "MAIL": MAIL,
        "COPYRIGHT": COPYRIGHT,
        "IT_BLOG": IT_BLOG,
        "CHEATSHEET": CHEATSHEET,
    }

    SEC_INFO = {
        "EDU": EDU,
        "EXP": EXP,
        "SKILL": SKILL,
        "RI": RI,
        "SIDE_PROJECT": SIDE_PROJECT,
        "BLOG_POST": BLOG_POST,
        "AWARD": AWARD,
        "PULL_REQUEST": PULL_REQUEST,
    }

    O_WEBPAGE = WEBPAGE_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, DEV_MODE=args.dev)
    O_WEBPAGE = tutils.html_formater(O_WEBPAGE)

    tutils.write(O_WEBPAGE, f"{WEBPAGE}/index.html")

    # O_CV_ENG = CV_ENG_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, COLOR="#b84646", LANG="english", WEIGTH=2)
    # tutils.write(O_CV_ENG, f"static/output/cv_eng.html")

    # O_CV_CHN = CV_ENG_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, COLOR="#DC3522", LANG="chinese", WEIGTH=2)
    # tutils.write(O_CV_CHN, f"static/output/cv_zh_tw.html")

    PERSONAL_INFO["SEEKING_POSITION"] = [x.replace("&", "\\&") for x in SEEKING_POSITION]
    PERSONAL_INFO["CURRENT_POSITION"] = CURRENT_POSITION.replace("&", "\\&")

    O_LATEX = LATEX_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, WEIGTH=1)
    tutils.write(O_LATEX, f"cv_eng.tex")
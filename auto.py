import argparse
import datetime
import os
import shutil

import requests

from core import tutils
from core.component import SkillTomlFile, TomlFile

# == personal information ============================================================================================
Q = "<div>The way lead to success is your own resolution.</div><div>得常咬菜根，即做百事成。</div>"

NAME = "Hsiang-Jen Li"
ZH_TW_NAME = "李享紝"
NICKNAME = "RN"

SEEKING_POSITION = [
    "Seeking a Data & MLOps Engineer role with a focus on research and complex data relationships",
    "Learning best through teaching",
    "Establishing development standards",
    "Standardizing development practices to automate CI/CD",
    "Unifying dev and deploy environments through Docker",
]
CURRENT_POSITION = "Finance & CS Background | Data Analyst @ SCSB"

GITHUB = "hsiangjenli"
MAIL = "hsiangjenli@gmail.com"
IT_BLOG = "https://hsiangjenli.github.io/blog/"
CHEATSHEET = "https://hsiangjenli.github.io/cheat-sheet/"
LINKEDIN = "hsiangjenli"

EDU = TomlFile.load("config/_education.toml").entries
EXP = TomlFile.load("config/_experience.toml").entries
SKILL = SkillTomlFile.load("config/_skill.toml").entries
RI = TomlFile.load("config/_research.toml").entries
SIDE_PROJECT = TomlFile.load("config/_project.toml").entries
PULL_REQUEST = tutils.load_toml("config/_open_source.toml")
AWARD = TomlFile.load("config/_award.toml").entries
BLOG_POST = requests.get("https://hsiangjenli.github.io/blog/api/getPosts/").json()[
    "data"
]["posts"]
# Filter out the post with [chatgpt] tag
BLOG_POST = [x for x in BLOG_POST if "[chatgpt]" not in x["title"].lower()]
# Sort the post by date
BLOG_POST = sorted(BLOG_POST, key=lambda x: x["date"], reverse=True)[:10]

# == webpage ==========================================================================================================
WEBPAGE = "hsiangjenli.github.io"
WEBPAGE_TEMPLATE = tutils.set_environemnt(
    folder="static/template/html/read_only", template="index.html"
)

# == CV ==============================================================================================================
CV_ENG_TEMPLATE = tutils.set_environemnt(
    folder="static/template/html/cv_eng", template="index.html"
)

# == latex ===========================================================================================================
LATEX_TEMPLATE = tutils.latex_set_environemnt(
    folder="static/template/latex", template="resume.tex"
)

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
    YEAR = (
        f"2024 ~ {datetime.datetime.now().year}"
        if datetime.datetime.now().year > 2024
        else 2024
    )
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
        "LINKEDIN": LINKEDIN,
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

    O_WEBPAGE = WEBPAGE_TEMPLATE.render(
        **PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, DEV_MODE=args.dev
    )
    # O_WEBPAGE = tutils.html_formater(O_WEBPAGE)

    tutils.write(O_WEBPAGE, f"{WEBPAGE}/index.html")

    # O_CV_ENG = CV_ENG_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, COLOR="#b84646", LANG="english", WEIGTH=2)
    # tutils.write(O_CV_ENG, f"static/output/cv_eng.html")

    # O_CV_CHN = CV_ENG_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, COLOR="#DC3522", LANG="chinese", WEIGTH=2)
    # tutils.write(O_CV_CHN, f"static/output/cv_zh_tw.html")

    # PERSONAL_INFO["SEEKING_POSITION"] = [
    #     x.replace("&", "\\&") for x in SEEKING_POSITION
    # ]
    # PERSONAL_INFO["CURRENT_POSITION"] = CURRENT_POSITION.replace("&", "\\&")

    # O_LATEX = LATEX_TEMPLATE.render(
    #     **PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, WEIGTH=1
    # )
    # tutils.write(O_LATEX, "cv_eng.tex")

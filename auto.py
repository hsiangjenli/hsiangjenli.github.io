import os
import shutil
import requests
import datetime
from core import tutils

# == personal information ============================================================================================
Q = "<div>The way lead to success is your own resolution.</div><div>得常咬菜根，即做百事成。</div>"

NAME = "Hsiang-Jen Li"
ZH_TW_NAME = "李享紝"
NICKNAME = "RN"
GITHUB = "hsiangjenli"
MAIL = "hsiangjenli@gmail.com"
IT_BLOG = "https://hsiangjenli.github.io/blog/"
CHEATSHEET = "https://hsiangjenli.github.io/cheat-sheet/"

EDU = tutils.load_toml("config/_education.toml")
EXP = tutils.load_toml("config/_experience.toml")
SKILL = tutils.load_toml("config/_skill.toml")
RI = tutils.load_toml("config/_research.toml")
SIDE_PROJECT = tutils.load_toml("config/_project.toml")
AWARD = tutils.load_toml("config/_award.toml")
BLOG_POST = requests.get("https://hsiangjenli.github.io/blog/api/getPosts/").json()['data']['posts']
BLOG_POST = sorted(BLOG_POST, key=lambda x: x['date'], reverse=True)

# == webpage ==========================================================================================================
WEBPAGE = "hsiangjenli.github.io"
WEBPAGE_TEMPLATE = tutils.set_environemnt(folder='static/template/html/read_only', template='index.html')

# == CV ==============================================================================================================
CV_ENG_TEMPLATE = tutils.set_environemnt(folder='static/template/html/cv_eng', template='index.html')
# == main ============================================================================================================
if __name__ == "__main__":
    
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
    }

    O_WEBPAGE = WEBPAGE_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE)
    tutils.write(O_WEBPAGE, f"{WEBPAGE}/index.html")

    O_CV_ENG = CV_ENG_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, COLOR="#b84646", LANG="english", WEIGTH=2)
    tutils.write(O_CV_ENG, f"static/output/cv_eng.html")

    O_CV_CHN = CV_ENG_TEMPLATE.render(**PERSONAL_INFO, **SEC_INFO, LAST_UPDATE=LAST_UPDATE, COLOR="#DC3522", LANG="chinese", WEIGTH=2)
    tutils.write(O_CV_CHN, f"static/output/cv_zh_tw.html")
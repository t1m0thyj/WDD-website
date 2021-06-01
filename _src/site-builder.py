import glob
import os
import sys
from datetime import datetime, timedelta

from mako.template import Template

from utils import load_themes_db

BASE_PATH = "https://cdn.jsdelivr.net/gh/t1m0thyj/WDD-website/themes/"
if len(sys.argv) > 1 and sys.argv[1] == "dev":
    BASE_PATH = ""

os.chdir(os.path.dirname(os.path.realpath(__file__)))
themes_db = load_themes_db()

for html_file in glob.glob("../themes/*.html"):
    os.remove(html_file)

print("Generating HTML files", end="")

three_months_ago = datetime.today() - timedelta(days=90)
for theme_id, theme_data in themes_db.items():
    theme_data["displayName"] = theme_data.get("displayName") or theme_id.replace("_", " ")
    theme_data["fileSize"] = round(theme_data["fileSize"] / 1024 / 1024, 2)
    theme_data["isNew"] = datetime.strptime(theme_data["dateAdded"], "%Y-%m-%d") > three_months_ago

    if theme_data["imageSize"][1] >= 4320:
        theme_data["imageSize"] = "8k"
    elif theme_data["imageSize"][1] >= 3384:
        theme_data["imageSize"] = "6k"
    elif theme_data["imageSize"][1] >= 2880:
        theme_data["imageSize"] = "5k"
    elif theme_data["imageSize"][1] >= 2160:
        theme_data["imageSize"] = "4k"
    elif theme_data["imageSize"][1] >= 1440:
        theme_data["imageSize"] = "2k"
    else:
        theme_data["imageSize"] = "HD"

macos_theme_data = {ti: td for ti, td in themes_db.items() if td["themeType"] == "macos"}
community_theme_data = {ti: td for ti, td in themes_db.items() if td["themeType"] == "community"}
paid_theme_data = {ti: td for ti, td in themes_db.items() if td["themeType"] == "paid"}

with open("themes-main.mako", "r") as fileobj:
    themes_main = Template(fileobj.read())

with open("../themes/index.html", "w", newline="\n") as fileobj:
    print(".", end="")
    fileobj.write(
        themes_main.render(
            basePath=BASE_PATH,
            macos_theme_data=macos_theme_data,
            community_theme_data=community_theme_data,
            paid_theme_data=paid_theme_data,
        )
    )

with open("themes-preview.mako", "r") as fileobj:
    themes_preview = Template(fileobj.read())

for theme_id, theme_data in themes_db.items():
    if theme_data["sunPhases"] is not None:
        print(".", end="")
        with open(f"../themes/preview_{theme_id}.html", "w", newline="\n") as fileobj:
            fileobj.write(themes_preview.render(basePath=BASE_PATH, themeId=theme_id, **theme_data))

print("done")

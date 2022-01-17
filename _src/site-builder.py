import json
import os
import sys

from mako.template import Template

from utils import load_themes_db

BASE_PATH = "../"
# BASE_PATH = "https://cdn.jsdelivr.net/gh/t1m0thyj/WDD-website/"
# if len(sys.argv) > 1 and sys.argv[1] == "dev":
#     BASE_PATH = "../"

os.chdir(os.path.dirname(os.path.realpath(__file__)))
themes_db = load_themes_db()

for html_file in os.listdir("../themes/preview"):
    os.remove(f"../themes/preview/{html_file}")

print("Generating HTML files", end="")

for theme_id, theme_data in themes_db.items():
    theme_data["displayName"] = theme_data.get("displayName") or theme_id.replace("_", " ")
    theme_data["fileSize"] = round(theme_data["fileSize"] / 1024 / 1024, 2)
    theme_data["themeType"] = theme_data["themeType"] if theme_data["themeType"] != "community" else "free"

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

with open("../themes/themes.db.js", "w", newline="\n") as fileobj:
    fileobj.write(f"var themesDb={json.dumps(themes_db)};")

with open("themes-main.mako", "r") as fileobj:
    themes_main = Template(fileobj.read())

with open("../themes/index.html", "w", newline="\n") as fileobj:
    print(".", end="")
    fileobj.write(
        themes_main.render(
            basePath=BASE_PATH,
            pageType="home",
            featuredFree=("24hr-Monterey-Bay-1", "24hr-BigSur-1", "24hr-Earth", "BitDay", "Firewatch", "Windows_11"),
            featuredPaid=("24hr-Canyonlands-1", "24hr-Monterey-Hills-1", "24hr-WhiteSands-1"),
            numFree=len([td for td in themes_db.values() if td["themeType"] == "free"]),
            numPaid=len([td for td in themes_db.values() if td["themeType"] == "paid"])
        )
    )

for theme_type in ("free", "paid", "macos"):
    with open(f"../themes/{theme_type}.html", "w", newline="\n") as fileobj:
        print(".", end="")
        fileobj.write(
            themes_main.render(
                basePath=BASE_PATH,
                pageType=theme_type
            )
        )

with open("themes-preview.mako", "r") as fileobj:
    themes_preview = Template(fileobj.read())

for theme_id, theme_data in themes_db.items():
    if theme_data["sunPhases"] is not None:
        print(".", end="")
        with open(f"../themes/preview/{theme_id}.html", "w", newline="\n") as fileobj:
            fileobj.write(
                themes_preview.render(
                    basePath=BASE_PATH if BASE_PATH.startswith("http") else (BASE_PATH + "../"),
                    themeId=theme_id,
                    **theme_data
                )
            )

print("done")

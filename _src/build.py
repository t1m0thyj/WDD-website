import glob
import json
import os
import sys

from mako.template import Template

with open(sys.argv[1], 'r') as fileobj:
    theme_db = json.load(fileobj)

os.chdir(os.path.dirname(os.path.realpath(__file__)))

for html_file in glob.glob("../themes/*.html"):
    os.remove(html_file)

print("Generating HTML files", end="")

with open("themes-new.txt", 'r') as fileobj:
    new_themes = fileobj.read().strip().splitlines()

for theme_id, theme_data in theme_db.items():
    theme_data["displayName"] = theme_data.get("displayName") or theme_id.replace("_", " ")
    theme_data["fileSize"] = round(theme_data["fileSize"] / 1024 / 1024, 2)
    theme_data["isNew"] = theme_id in new_themes

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

photos_theme_data = {ti: td for ti, td in theme_db.items() if td["themeType"] == "photos"}
art_theme_data = {ti: td for ti, td in theme_db.items() if td["themeType"] == "art"}
paid_theme_data = {ti: td for ti, td in theme_db.items() if td["themeType"] == "paid"}

with open("themes-main.mako", 'r') as fileobj:
    themes_main = Template(fileobj.read())

with open("../themes/index.html", 'w') as fileobj:
    print(".", end="")
    fileobj.write(themes_main.render(photos_theme_data=photos_theme_data, art_theme_data=art_theme_data,
        paid_theme_data=paid_theme_data))

with open("themes-preview.mako", 'r') as fileobj:
    themes_preview = Template(fileobj.read())

for theme_id, theme_data in theme_db.items():
    if not theme_id.startswith("24hr"):
        print(".", end="")
        with open(f"../themes/preview_{theme_id}.html", 'w') as fileobj:
            fileobj.write(themes_preview.render(themeId=theme_id, **theme_data))

print("done")

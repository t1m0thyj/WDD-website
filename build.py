import json
import os

from mako.template import Template

for filename in os.listdir("scripts"):
    if os.path.isfile(f"scripts/{filename}"):
        os.remove(os.path.join("scripts", filename))

with open("script-data.json", 'r') as fileobj:
    script_data = json.load(fileobj)

with open("scripts.mako", 'r') as fileobj:
    scripts_template = Template(fileobj.read())

with open("scripts/index.html", 'w') as fileobj:
    fileobj.write(scripts_template.render(scripts_stable=script_data["stable"],
        scripts_experimental=script_data["experimental"]))

print("Generated scripts page:", "./scripts/index.html")

for filename in os.listdir("themes"):
    if os.path.isfile(f"themes/{filename}"):
        os.remove(os.path.join("themes", filename))

with open("theme-data.json", 'r') as fileobj:
    theme_data = json.load(fileobj)

with open("themes-new.txt", 'r') as fileobj:
    new_themes = fileobj.read().strip().splitlines()

with open("themes-main.mako", 'r') as fileobj:
    themes_main = Template(fileobj.read())

with open("themes/index.html", 'w') as fileobj:
    fileobj.write(themes_main.render(new_themes=new_themes, themes_free=theme_data["free"],
        themes_paid=theme_data["paid"]))

with open("themes-preview.mako", 'r') as fileobj:
    themes_preview = Template(fileobj.read())

for td in theme_data["free"]:
    theme_name, theme_type = td[:2]

    if theme_type == "contrib":
        with open(f"themes/{theme_name}.html", 'w') as fileobj:
            fileobj.write(themes_preview.render(theme_data=td))

print("Generated themes page:", "./themes/index.html")

import json
import os

from mako.template import Template

for filename in os.listdir("themes"):
    if os.path.isfile(f"themes/{filename}"):
        os.remove(os.path.join("themes", filename))

with open("theme-data.json", 'r') as fileobj:
    theme_data = json.load(fileobj)

with open("new-themes.txt", 'r') as fileobj:
    new_themes = fileobj.read().strip().splitlines()

with open("main.mako", 'r') as fileobj:
    template_main = Template(fileobj.read())

with open("themes/index.html", 'w') as fileobj:
    fileobj.write(template_main.render(new_themes=new_themes, themes_free=theme_data["free"],
        themes_paid=theme_data["paid"]))

with open("preview.mako", 'r') as fileobj:
    template_preview = Template(fileobj.read())

for td in theme_data["free"]:
    theme_name, theme_type = td[:2]

    if theme_type == "contrib":
        with open(f"themes/{theme_name}.html", 'w') as fileobj:
            fileobj.write(template_preview.render(theme_data=td))

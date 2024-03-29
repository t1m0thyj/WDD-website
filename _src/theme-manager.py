import os
import re
import sys
from datetime import datetime

from utils import (
    extract_ddw,
    get_md5_checksum,
    get_theme_url,
    load_theme_config,
    load_themes_db,
    make_previews,
    make_thumbnails,
    mediafire_download,
    save_themes_db,
)

# TODO Automate macOS themes process - take HEIC, make regular & square DDW, gen 50-50 thumbs
# TODO Implement function to remove themes
orig_cwd = os.getcwd()


def add(theme_type, theme_path, theme_id=None):
    is_local = re.match("\w{2,}:", theme_path) is None
    theme_path = theme_path if not is_local or os.path.isabs(theme_path) else os.path.join(orig_cwd, theme_path)
    ddw_file = theme_path if is_local else mediafire_download(theme_path)
    theme_dir = extract_ddw(ddw_file)
    theme_config = load_theme_config(theme_dir)
    themes_db = load_themes_db()
    theme_id = theme_id or os.path.splitext(os.path.basename(ddw_file))[0].replace(" " if is_local else "+", "_")
    if "#" in theme_id:
        theme_config["displayName"] = theme_config.get("displayName", theme_id.replace("_", " "))
        theme_id = theme_id.replace("#", "")
    if "&" in theme_id:
        theme_config["displayName"] = theme_config.get("displayName", theme_id.replace("_", " "))
        theme_id = theme_id.replace("&", "and")
    if theme_id in themes_db:
        raise ValueError(f"Theme already exists in database: {theme_id}")
    themes_db[theme_id] = {
        "themeUrl": theme_path if not is_local else get_theme_url(theme_type, theme_id),
        "themeType": theme_type,
        "displayName": theme_config.get("displayName"),
        "imageCredits": theme_config.get("imageCredits"),
        "fileHash": get_md5_checksum(ddw_file),
        "fileSize": os.path.getsize(ddw_file),
        "dateAdded": str(datetime.utcfromtimestamp(os.path.getmtime(ddw_file)).date()),
        "imageSize": make_thumbnails(theme_config, theme_dir, theme_id),
        "sunPhases": make_previews(theme_config, theme_dir, theme_id) if not theme_id.startswith("24hr") else None,
    }
    if theme_id.startswith("24hr") and theme_type == "community":
        themes_db[theme_id]["displayName"] = "24 Hour " + themes_db[theme_id]["displayName"]
    save_themes_db(themes_db)


def remove(theme_id):
    pass


os.chdir(os.path.dirname(os.path.realpath(__file__)))

if len(sys.argv) > 2:
    action = sys.argv[1]
    if action == "add":
        type_ = sys.argv[2]
        theme_paths = sys.argv[3:]
        if not theme_paths:
            with open("new-themes.csv", 'r') as fileobj:
                theme_paths = [line.strip() for line in fileobj if not line.startswith("#")]
        for path in theme_paths:
            args = path.split(" ")
            print(f"+ {type_}\t{args[0]}")
            add(type_, *args)
    elif action == "remove":
        for id_ in sys.argv[2:]:
            print(f"- {id_}")
            remove(id_)

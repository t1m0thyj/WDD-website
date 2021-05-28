import os
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


def add(theme_type, theme_path):
    is_local = os.path.isfile(theme_path)
    ddw_file = theme_path if is_local else mediafire_download(theme_path)
    theme_dir = extract_ddw(ddw_file)
    theme_config = load_theme_config(theme_dir)
    themes_db = load_themes_db()
    theme_id = os.path.splitext(os.path.basename(ddw_file))[0].replace(" ", "_")
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


old_cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if len(sys.argv) > 2:
    action = sys.argv[1]
    if action == "add":
        type_ = sys.argv[2]
        for path in sys.argv[3:]:
            print(f"+ {type_}\t{path}")
            add(type_, path if os.path.isabs(path) else os.path.join(old_cwd, path))
    elif action == "remove":
        for id_ in sys.argv[2:]:
            print(f"- {id_}")
            remove(id_)

import glob
import hashlib
import json
import os
import re
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile

from bs4 import BeautifulSoup
from PIL import Image
import requests
import yaml


def extract_ddw(ddw_file):
    out_dir = os.path.join(tempfile.gettempdir(), os.path.splitext(os.path.basename(ddw_file))[0])
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    with zipfile.ZipFile(ddw_file, "r") as fileobj:
        fileobj.extractall(out_dir)
    return out_dir


def get_image_ids(theme_config):
    image_ids = []
    if theme_config.get("sunriseImageList"):
        image_ids.extend(theme_config["sunriseImageList"])
    image_ids.extend(theme_config["dayImageList"])
    if theme_config.get("sunsetImageList"):
        image_ids.extend(theme_config["sunsetImageList"])
    image_ids.extend(theme_config["nightImageList"])
    return set(image_ids)


def get_middle_item(lst):
    return lst[len(lst) // 2] if lst else -1


def get_md5_checksum(filename):
    with open(filename, "rb") as fileobj:
        data = fileobj.read()
    return hashlib.md5(data).hexdigest()


def get_theme_url(theme_type, theme_id):
    with open("themes.yaml", "r") as fileobj:
        themes_yaml = yaml.safe_load(fileobj)
    return themes_yaml[theme_type][theme_id][0]


def load_theme_config(theme_dir):
    with open(next(glob.iglob(theme_dir + "/*.json")), "r") as fileobj:
        return json.load(fileobj)


def load_themes_db():
    if not os.path.isfile("themes.db.json"):
        return {}

    with open("themes.db.json", "r") as fileobj:
        return json.load(fileobj)


def make_previews(theme_config, theme_dir, theme_id):
    sunrise_image_id = get_middle_item(theme_config.get("sunriseImageList"))
    day_image_id = theme_config.get("dayHighlight") or get_middle_item(theme_config["dayImageList"])
    sunset_image_id = get_middle_item(theme_config.get("sunsetImageList"))
    night_image_id = theme_config.get("nightHighlight") or get_middle_item(theme_config["nightImageList"])

    image_filenames = {}
    if sunrise_image_id != -1 and sunrise_image_id != day_image_id and sunrise_image_id != night_image_id:
        image_filenames["sunrise"] = theme_config["imageFilename"].replace("*", str(sunrise_image_id))
    image_filenames["day"] = theme_config["imageFilename"].replace("*", str(day_image_id))
    if sunset_image_id != -1 and sunset_image_id != day_image_id and sunset_image_id != night_image_id:
        image_filenames["sunset"] = theme_config["imageFilename"].replace("*", str(sunset_image_id))
    image_filenames["night"] = theme_config["imageFilename"].replace("*", str(night_image_id))

    for phase, filename in image_filenames.items():
        img = Image.open(f"{theme_dir}/{filename}")
        img = resize_16x9(img, 1920)
        img.save(f"../images/previews/{theme_id}_{phase}.jpg", quality=75)

    return list(image_filenames.keys())


def make_thumbnails(theme_config, theme_dir, theme_id):
    light_image_id = theme_config.get("dayHighlight") or get_middle_item(theme_config["dayImageList"])
    light_image_filename = theme_config["imageFilename"].replace("*", str(light_image_id))
    dark_image_id = theme_config.get("nightHighlight") or get_middle_item(theme_config["nightImageList"])
    dark_image_filename = theme_config["imageFilename"].replace("*", str(dark_image_id))

    img1 = Image.open(f"{theme_dir}/{light_image_filename}")
    w, h = img1.size
    img1 = resize_16x9(img1, 384)
    img1.save(f"../images/thumbnails/{theme_id}_day.png")

    img2 = Image.open(f"{theme_dir}/{dark_image_filename}")
    img2 = resize_16x9(img2, 384)
    img2.save(f"../images/thumbnails/{theme_id}_night.png")

    return (w, h)


def mediafire_download(theme_url, api_key=None):
    out_file = os.path.join(tempfile.gettempdir(),
        re.search(r"mediafire\.com/file/.+?/(.+?)($|/file)", theme_url).group(1))
    if api_key is None:
        headers = {"User-Agent": "Mozilla/5.0"}
        with urllib.request.urlopen(urllib.request.Request(theme_url, headers=headers)) as fileobj:
            html = fileobj.read()
    else:
        rapidapi_host = "scrapeninja.p.rapidapi.com"
        headers = {
            "X-RapidApi-Key": api_key,
            "X-RapidApi-Host": rapidapi_host,
            "Content-Type": "application/json"
        }
        response = requests.post(f"https://{rapidapi_host}/scrape", json={"url": theme_url}, headers=headers).json()
        if response["info"]["statusCode"] != 200:
            info = response["info"]
            raise urllib.error.HTTPError(theme_url, info["statusCode"], info["statusMessage"], info["headers"])
        html = response["body"]
    soup = BeautifulSoup(html, "html.parser")
    direct_link = soup.find("a", {"id": "downloadButton"})["href"]
    urllib.request.urlretrieve(direct_link, out_file)
    return out_file


def resize_16x9(img, width):
    w, h = img.size
    if (w / h) > (16 / 9):  # Too wide
        w2 = int(h * 16 / 9)
        x = (w - w2) / 2
        img = img.crop((x, 0, x + w2, h))
    elif (w / h) < (16 / 9):  # Too high
        h2 = int(w * 9 / 16)
        y = (h - h2) / 2
        img = img.crop((0, y, w, y + h2))
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img.resize((width, int(width * 9 / 16)))


def save_themes_db(themes_db):
    get_theme_key = lambda ti, td: td.get("displayName") or ti.replace(" ", "_")
    sorted_db = dict(sorted(themes_db.items(), key=lambda theme: get_theme_key(*theme).lower()))
    with open("themes.db.json", "w", newline="\n") as fileobj:
        json.dump(sorted_db, fileobj, indent=4)

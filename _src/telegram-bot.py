import logging
import os
import re
import smtplib
import threading
import traceback
import urllib.error
import zipfile
from dataclasses import dataclass
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

import telebot
from dotenv import load_dotenv
from PIL import Image, ImageStat

from utils import extract_ddw, get_image_ids, get_middle_item, load_theme_config, mediafire_download, resize_16x9

EMOJI_APPROVED = "✔️"
EMOJI_REJECTED = "❌"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


@dataclass
class ThemeData:
    theme_name: str
    theme_url: str
    ddw_file: str
    theme_dir: str
    theme_config: dict
    fatal_error: bool


def validate_ddw_name(data: ThemeData):
    filename = re.search(r"mediafire\.com/file/.+?/(.+?)($|/file)", data.theme_url).group(1)
    if re.sub("[\W_]", "", os.path.splitext(filename)[0]) != re.sub("[\W_]", "", data.theme_name):
        return 'DDW filename matches theme name (e.g., "My_Theme.ddw" for "My Theme")'


def validate_ddw_contents(data: ThemeData):
    actual_files = set(os.listdir(data.theme_dir))
    expected_files = set([next((f for f in actual_files if f.endswith(".json")), "theme.json")])
    for i in get_image_ids(data.theme_config):
        expected_files.add(data.theme_config["imageFilename"].replace("*", str(i)))

    data.fatal_error = not all(os.path.isfile(f"{data.theme_dir}/{filename}") for filename in expected_files)
    if expected_files != actual_files:
        return 'DDW file contains only "theme.json" and all image files it references'


def validate_image_credits(data: ThemeData):
    credits = data.theme_config.get("imageCredits")
    if not credits or credits == "Created by the .ddw Theme Creator":
        return "Image credits include name of original artist or photographer"


def validate_image_size(data: ThemeData):
    image_filename = data.theme_config["imageFilename"].replace("*", str(data.theme_config["dayImageList"][0]))
    img = Image.open(f"{data.theme_dir}/{image_filename}")
    w, h = img.size
    if w < 1920 or h < 1080:
        return "Image size is full HD resolution (1920x1080) or higher"


def validate_image_ratio(data: ThemeData):
    image_filename = data.theme_config["imageFilename"].replace("*", str(data.theme_config["dayImageList"][0]))
    img = Image.open(f"{data.theme_dir}/{image_filename}")
    w, h = img.size
    if w < h:
        return "Image ratio is landscape or square (16:9 is recommended)"


def validate_image_brightness(data: ThemeData):
    image_data = {}
    for i in get_image_ids(data.theme_config):
        image_filename = data.theme_config["imageFilename"].replace("*", str(i))
        img = Image.open(f"{data.theme_dir}/{image_filename}").convert("L")
        img_stat = ImageStat.Stat(img)
        image_data[i] = img_stat.mean[0]

    brightest_ids = [k for k, v in image_data.items() if k in data.theme_config["dayImageList"] and
        v == max(image_data.values())]
    darkest_ids = [k for k, v in image_data.items() if k in data.theme_config["nightImageList"] and
        v == min(image_data.values())]
    if not brightest_ids or not darkest_ids:
        return "Brightest image is shown at noon and darkest image is shown at midnight"


class MyClient():
    def __init__(self, *args, **kwargs):
        telebot.apihelper.SESSION_TIME_TO_LIVE = 5 * 60
        self.bot = telebot.TeleBot(*args, **kwargs)
    
    def start(self):
        self.bot.channel_post_handler(func=lambda message: True)(self.on_message)
        self.on_ready()
        self.bot.polling()

    def on_ready(self):
        print(f"Logged in as {self.bot.user.full_name} (ID: {self.bot.user.id})")
        print("------")

    def on_message(self, message: telebot.types.Message):
        if message.chat.id != int(os.environ["TELEGRAM_CHANNEL_ID"]):
            return
        elif not message.text.startswith("New theme submitted by"):
            return

        threading.Thread(target=self.theme_handler, args=(message,)).start()

    def theme_handler(self, message: telebot.types.Message):
        try:
            lines = [line for line in message.text.splitlines() if line]
            email_address = lines[0].split()[-1]
            theme_name = lines[1].split(": ")[1].strip("`")
            theme_url = lines[2].split(": ")[1]

            logging.info(f"[{theme_name}] Theme submitted")
            data, errors = MyClient.check_theme(theme_name, theme_url)

            self.send_email(errors, email_address, theme_name)
            self.bot.send_message(message.chat.id, self.get_new_message(errors, theme_name), parse_mode="MarkdownV2", reply_to_message_id=message.message_id)
            if not errors:
                self.send_approved_email(data)
                with open("new-themes.csv", 'a') as fileobj:
                    fileobj.writelines([theme_url])
                logging.info(f"[{theme_name}] Theme approved")
            else:
                for error in errors:
                    logging.error(f"[{theme_name}] {error}")
                logging.info(f"[{theme_name}] Theme rejected")
        except Exception as e:
            logging.error(e, exc_info=True)
            self.bot.send_message(os.environ["OWNER_TELEGRAM_ID"], f"```\n{traceback.format_exc()}\n```", parse_mode="MarkdownV2")

    @staticmethod
    def check_theme(theme_name, theme_url):
        try:
            ddw_file = mediafire_download(theme_url)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, ["Theme URL is a valid MediaFire link"]
            raise e
        except:
            raise

        try:
            theme_dir = extract_ddw(ddw_file)
        except zipfile.BadZipFile:
            return None, ["DDW file is a valid ZIP archive"]
        except:
            raise

        try:
            theme_config = load_theme_config(theme_dir)
        except:
            return None, ["Theme config is a valid JSON file"]

        data = ThemeData(theme_name, theme_url, ddw_file, theme_dir, theme_config, False)
        errors = []

        for validator in (
            validate_ddw_name,
            validate_ddw_contents,
            validate_image_credits,
            validate_image_size,
            validate_image_ratio,
            validate_image_brightness,
        ):
            errors.append(validator(data))
            if data.fatal_error:
                break

        return data, [error for error in errors if error]

    def send_email(self, errors, recipient, theme_name):
        if errors:
            subject = f"{EMOJI_REJECTED} Theme Rejected"
            body = f'Your WinDynamicDesktop theme "{theme_name}" has been rejected.\n\n'
            body += "Please fix the following checks that have failed before resubmitting your theme:\n"
            body += "\n".join(f"\t{EMOJI_REJECTED} {error}" for error in errors)
        else:
            subject = f"{EMOJI_APPROVED} Theme Approved"
            body = f'Your WinDynamicDesktop theme "{theme_name}" has been automatically approved.\n\n'
            body += "Please allow up to a week for manual approval and your theme to be added to the website."

        message = MIMEText(body, "plain", "utf-8")
        message.add_header("Subject", subject)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(os.environ["SMTP_EMAIL"], os.environ["SMTP_PASSWORD"])
            server.sendmail(os.environ["SMTP_EMAIL"], recipient, message.as_string())

    def get_new_message(self, errors, theme_name):
        lines = []
        escape_md = lambda text: re.sub(r'([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])', r'\\\1', text)

        if errors:
            lines.append(f"{EMOJI_REJECTED} *Theme Rejected*")
            lines.append(f"{len(errors)} check\(s\) failed for *{escape_md(theme_name)}*")
            lines.extend(f"\- {escape_md(error)}" for error in errors)
        else:
            lines.append(f"{EMOJI_APPROVED} *Theme Approved*")
            lines.append(f"Check email for *{escape_md(theme_name)}*")

        return "\n".join(lines)

    def send_approved_email(self, data: ThemeData):
        message = MIMEMultipart("related")
        message.add_header("Subject", "New Theme Approved")

        html = f"""
<html>
<body>
    <p><b>Theme Name:</b> {data.theme_name}</p>
    <p><b>Theme URL:</b> <a href="{data.theme_url}">{data.theme_url}</a></p>
    <img src="cid:image1" style="width: 384px; height: auto; display: inline-block; margin-right: 5px;">
    <img src="cid:image2" style="width: 384px; height: auto; display: inline-block;">
</body>
</html>
"""
        message.attach(MIMEText(html, "html"))

        day_highlight = data.theme_config.get("dayHighlight") or get_middle_item(data.theme_config["dayImageList"])
        image_filename = data.theme_config["imageFilename"].replace("*", str(day_highlight))
        day_img = BytesIO()
        resize_16x9(Image.open(f"{data.theme_dir}/{image_filename}"), 384).save(day_img, format="PNG")
        day_img.seek(0)
        mime_image1 = MIMEImage(day_img.read())
        mime_image1.add_header("Content-ID", "<image1>")
        message.attach(mime_image1)

        night_highlight = data.theme_config.get("nightHighlight") or get_middle_item(
            data.theme_config["nightImageList"]
        )
        image_filename = data.theme_config["imageFilename"].replace("*", str(night_highlight))
        night_img = BytesIO()
        resize_16x9(Image.open(f"{data.theme_dir}/{image_filename}"), 384).save(night_img, format="PNG")
        night_img.seek(0)
        mime_image2 = MIMEImage(night_img.read())
        mime_image2.add_header("Content-ID", "<image2>")
        message.attach(mime_image2)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(os.environ["SMTP_EMAIL"], os.environ["SMTP_PASSWORD"])
            server.sendmail(os.environ["SMTP_EMAIL"], os.environ["OWNER_EMAIL"], message.as_string())


logging.basicConfig(level=logging.INFO)
load_dotenv()
MyClient(os.environ["TELEGRAM_TOKEN"]).start()

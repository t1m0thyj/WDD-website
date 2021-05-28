import os
import re
import smtplib
from dataclasses import dataclass
from email.mime.text import MIMEText
from io import BytesIO

import discord
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


def validate_ddw_name(data: ThemeData):
    filename = re.search(r"mediafire\.com/file/.+?/(.+?)($|/file)", data.theme_url).group(1)
    if re.split("[\W_]+", os.path.splitext(filename)[0]) != re.split("[\W_]+", data.theme_name):
        return 'DDW filename matches theme name (e.g., "My_Theme.ddw" for "My Theme")'


def validate_ddw_contents(data: ThemeData):
    expected_files = set(["theme.json"])
    for i in get_image_ids(data.theme_config):
        expected_files.add(data.theme_config["imageFilename"].replace("*", str(i)))

    if set(os.listdir(data.theme_dir)) != expected_files:
        return 'DDW file contains "theme.json" and all image files it references'


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

    brightest_id = max(image_data, key=image_data.get)
    darkest_id = min(image_data, key=image_data.get)
    if brightest_id not in data.theme_config["dayImageList"] or darkest_id not in data.theme_config["nightImageList"]:
        return "Brightest image is shown at noon and darkest image is shown at midnight"


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def on_message(self, message):
        if message.channel.id == int(os.environ["DISCORD_CHANNEL_NEW_ID"]) and message.webhook_id is not None:
            email_address = re.search("^Email Address: (.+)$", message.content, re.MULTILINE).group(1)
            theme_name = re.search("^Theme Name: (.+)$", message.content, re.MULTILINE).group(1)
            theme_url = re.search("^Theme URL: (.+)$", message.content, re.MULTILINE).group(1)
            data, errors = await self.check_theme(theme_name, theme_url)

            await self.send_email(errors, email_address, theme_name)
            await message.reply(**self.get_new_message(errors, theme_name))
            if not errors:
                approved_channel = self.get_channel(int(os.environ["DISCORD_CHANNEL_APPROVED_ID"]))
                await approved_channel.send(**self.get_approved_message(data))

    async def check_theme(self, theme_name, theme_url):
        print(f"Checking {theme_name}: {theme_url}")
        errors = []

        try:
            ddw_file = mediafire_download(theme_url)
        except:
            errors.append("Theme URL is a valid MediaFire link")

        try:
            theme_dir = extract_ddw(ddw_file)
        except:
            errors.append("DDW file is a valid ZIP archive")

        try:
            theme_config = load_theme_config(theme_dir)
        except:
            errors.append("Theme config is a valid JSON file")

        data = ThemeData(theme_name, theme_url, ddw_file, theme_dir, theme_config)
        if errors:
            return data, errors

        for validator in (
            validate_ddw_name,
            validate_ddw_contents,
            validate_image_credits,
            validate_image_size,
            validate_image_ratio,
            validate_image_brightness,
        ):
            errors.append(validator(data))

        return data, [error for error in errors if error]

    async def send_email(self, errors, recipient, theme_name):
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
        embed = discord.Embed()

        if errors:
            embed.title = f"{EMOJI_REJECTED} Theme Rejected"
            embed.description = "\n".join(f"\t{EMOJI_REJECTED} {error}" for error in errors)
            embed.set_footer(text=theme_name)
        else:
            embed.title = f"{EMOJI_APPROVED} Theme Approved"
            approved_channel = self.get_channel(int(os.environ["DISCORD_CHANNEL_APPROVED_ID"]))
            embed.description = f"Check {approved_channel.mention} for **{theme_name}**"

        return {"embed": embed}

    def get_approved_message(self, data):
        content = f"{data.theme_name}: {data.theme_url}"
        files = []

        day_highlight = data.theme_config.get("dayHighlight") or get_middle_item(data.theme_config["dayImageList"])
        image_filename = data.theme_config["imageFilename"].replace("*", str(day_highlight))
        day_img = BytesIO()
        resize_16x9(Image.open(f"{data.theme_dir}/{image_filename}"), 384).save(day_img, format="PNG")
        day_img.seek(0)
        files.append(discord.File(day_img, "day.png"))

        night_highlight = data.theme_config.get("nightHighlight") or get_middle_item(
            data.theme_config["nightImageList"]
        )
        image_filename = data.theme_config["imageFilename"].replace("*", str(night_highlight))
        night_img = BytesIO()
        resize_16x9(Image.open(f"{data.theme_dir}/{image_filename}"), 384).save(night_img, format="PNG")
        night_img.seek(0)
        files.append(discord.File(night_img, "night.png"))

        return {"content": content, "files": files}


load_dotenv()
client = MyClient()
client.run(os.environ["DISCORD_TOKEN"])

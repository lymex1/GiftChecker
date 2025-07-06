import os
import time
import asyncio
import requests

from telethon.tl.types import StarGift
from telethon import TelegramClient, functions

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = os.getenv("SESSION", "session_name")
bot_token = os.getenv("BOT_TOKEN")
topic = os.getenv("NTFY_TOPIC")

client = TelegramClient(f'/data/bot_session}', api_id, api_hash)

known_ids = set()

async def check_new_gifts():
    global known_ids
    try:
        result = await client(functions.payments.GetStarGiftsRequest(hash=0))
        current_ids = {gift.id for gift in result.gifts}
        new_ids = current_ids - known_ids

        if new_ids:
            print("🎁 Новые подарки обнаружены:")
            known_ids = current_ids
            for _ in range(50):
                requests.post(f"https://ntfy.sh/{topic}", data="🎁 Вышел новый Telegram подарок!".encode("utf-8"))
                time.sleep(0.03)
        else:
            print("✅ Новых подарков нет.")
    except Exception as e:
        print("⚠️ Ошибка:", e)
        requests.post(f"https://ntfy.sh/{topic}", data=f"❌ Ошибка в скрипте: {e}".encode("utf-8"))

async def main():
    try:
        await client.start(bot_token=bot_token)
        result = await client(functions.payments.GetStarGiftsRequest(hash=0))
        global known_ids
        known_ids = {gift.id for gift in result.gifts}
        print(f"🎁 Загружено {len(known_ids)} известных подарков.")
    except Exception as e:
        print("⚠️ Ошибка при первом запуске:", e)
        requests.post(f"https://ntfy.sh/{topic}", data=f"❌ Ошибка при старте: {e}".encode("utf-8"))
        return

    while True:
        await check_new_gifts()
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import requests
import time
from telethon.tl.types import StarGift
from telethon import TelegramClient, functions

api_id = 23919006 
api_hash = '6b4e3658f9b2866f0c3f711decc326c3'

client = TelegramClient('session_name', api_id, api_hash)

known_ids = set()

async def check_new_gifts():
    global known_ids
    result = await client(functions.payments.GetStarGiftsRequest(hash=0))
    current_ids = {gift.id for gift in result.gifts}

    new_ids = current_ids - known_ids
    
    topic = "star-gifts-2025"
    message = "🎁 Вышел новый Telegram подарок!"
    
    if new_ids:
        print("🎁 Новые подарки обнаружены:")
        known_ids = current_ids
        for _ in range(30):
            requests.post(f"https://ntfy.sh/{topic}", data=message.encode("utf-8"))
            time.sleep(0.03)
    else:
        print("✅ Новых подарков нет.")


async def main():
    await client.start()
    result = await client(functions.payments.GetStarGiftsRequest(hash=0))
    global known_ids
    known_ids = {gift.id for gift in result.gifts}
    print(f"🎁 Загружено {len(known_ids)} известных подарков.")

    while True:
        await check_new_gifts()
        await asyncio.sleep(10)

asyncio.run(main())

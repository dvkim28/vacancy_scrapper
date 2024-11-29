# import os
#
# import aiohttp
#
# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# CHAT_ID = os.environ.get("CHAT_ID")
#
#
# async def send_telegram_message(vac_data: dict):
#     if not BOT_TOKEN or not CHAT_ID:
#         print("BOT_TOKEN or CHAT_ID is not set.")
#         return
#
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
#     message = (
#         f"There is new vacation: {vac_data['title']}\n"
#         f"Platform: {vac_data['source']}\n"
#         f"Company: {vac_data['company']}\n"
#         f"Description: {vac_data['description']}\n"
#         f"Link: {vac_data['url']}"
#     )
#
#     params = {"chat_id": CHAT_ID, "text": message}
#
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, params=params) as response:
#                 if response.status == 200:
#                     print("Telegram message sent.")
#                 else:
#                     print("Telegram message failed.")
#     except Exception as e:
#         print(f"Error: {e}")

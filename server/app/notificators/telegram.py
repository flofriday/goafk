from app.config import get_settings
from ..models import User
import aiohttp

telegram_token = get_settings().telegram_bot_token
api_base_url = f"https://api.telegram.org/bot{telegram_token}/"


async def send_text(user: User, text: str) -> int:
    async with aiohttp.ClientSession() as client:
        async with client.get(
            api_base_url + "sendMessage",
            data={
                "chat_id": int(user.user_name),
                "text": text,
                "disable_web_page_preview": True,
            },
        ) as response:
            return response.status


async def send_image_url(user: User, image_url: str, caption: str) -> int:
    async with aiohttp.ClientSession() as client:
        async with client.get(
            api_base_url + "sendPhoto",
            data={
                "chat_id": int(user.user_name),
                "photo": image_url,
                "caption": caption,
                "disable_web_page_preview": True,
            },
        ) as response:
            return response.status

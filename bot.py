import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("bot")


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        log.error("Error: %s. Бот не запущен.", name)
        raise SystemExit(1)
    return value


async def on_start(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else "?"
    log.info("/start от user_id=%s", user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Open Step2Eat Mini App",
                    web_app=WebAppInfo(url=os.getenv("MINI_APP_URL")),
                )
            ]
        ]
    )
    await message.answer(
        "Press the button below to open the app 👇",
        reply_markup=keyboard,
    )

async def main() -> None:
    token = require_env("BOT_TOKEN")
    mini_app_url = require_env("MINI_APP_URL")
    log.info("Переменная окружения проверяется...")
    log.info("GOOD - MINI_APP_URL: %s", mini_app_url)

    bot = Bot(token)
    try:
        me = await bot.get_me()
    except Exception:
        log.exception("Error: No c0nnetct to telegram, Check TG token or network")
        raise SystemExit(1)

    log.info("GOOD.Работает: @%s (id=%s).", me.username, me.id)

    dp = Dispatcher()
    dp.message.register(on_start, CommandStart())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

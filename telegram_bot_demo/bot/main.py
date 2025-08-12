import asyncio
import logging
import os
from typing import Union
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv
from database import Database
from message_handler import MessageHandler

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHANNEL_ID = os.getenv("CHANNEL_ID")
DATABASE_URL = os.getenv("DATABASE_URL")

if not all([BOT_TOKEN, WEBHOOK_URL, CHANNEL_ID, DATABASE_URL]):
    raise ValueError("Не все обязательные переменные окружения установлены")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

db = Database(DATABASE_URL)
message_handler = MessageHandler(bot, db, CHANNEL_ID)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для пересылки сообщений. "
        "Просто отправьте мне любое сообщение, и я перешлю его в канал."
    )


@dp.message()
async def handle_message(message: Message):
    try:
        if message.chat.type == "private":
            await message_handler.handle_user_message(message)
        elif message.chat.type == "channel":
            await message_handler.handle_channel_reply(message)
        else:
            logger.info(f"Игнорируем сообщение из {message.chat.type}: {message.chat.id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        if message.chat.type == "private":
            await message.answer("❌ Произошла ошибка при обработке вашего сообщения.")


async def on_startup(app):
    logger.info("Бот запускается...")
    
    await db.init()
    
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )
    logger.info(f"Webhook установлен: {WEBHOOK_URL}")


async def on_shutdown():
    logger.info("Бот останавливается...")
    
    await bot.delete_webhook()

    await bot.session.close()
    await db.close()


def main():
    app = web.Application()
    
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_handler.register(app, path="/webhook")
    
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(
        app,
        host="0.0.0.0",
        port=8000
    )


if __name__ == "__main__":
    main()

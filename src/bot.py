import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp import WebhookRequestHandler, get_new_configured_app
from aiohttp import web
from config import config
from handlers.commands import router as commands_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN_BOT)
storage = RedisStorage.from_url(config.REDIS_URL)
dp = Dispatcher(bot, storage=storage)
dp.include_router(commands_router)

async def on_startup(dp: Dispatcher):
    await bot.set_webhook(config.WEBHOOK_URL)
    logging.info(f"Webhook set to {config.WEBHOOK_URL}")

async def on_shutdown(dp: Dispatcher):
    logging.info("Removing webhook")
    await bot.delete_webhook()

def main():
    app = get_new_configured_app(dp, WebhookRequestHandler)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host=config.WEBHOOK_HOST, port=config.WEBHOOK_PORT)

if __name__ == '__main__':
    main()

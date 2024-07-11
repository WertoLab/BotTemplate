import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from config import config
from handlers.commands import router as commands_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN_BOT)
dp = Dispatcher()

dp.include_router(commands_router)


async def on_startup(app: web.Application):
    await bot.set_webhook(config.WEBHOOK_URL)
    logging.info(f"Webhook set to {config.WEBHOOK_URL}")


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    logging.info("Webhook removed")


def main():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path='/webhook')

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    setup_application(app, dp)

    web.run_app(app, host=config.WEBHOOK_HOST, port=config.WEBHOOK_PORT)


if __name__ == '__main__':
    main()

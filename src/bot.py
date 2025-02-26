import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import web
from config import config
from handlers import start_router, add_paper_router, handle_text_router
from handlers.callbacks import (
    send_title_router,
    view_papers_router,
    delete_paper_router,
    help_router,
    back_to_main_router,
    select_paper_router
)
from database import setup_redis, shutdown_redis, redis_client
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import Update
from aiogram.exceptions import TelegramBadRequest

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN_BOT, default=DefaultBotProperties(parse_mode='HTML'))

async def on_startup(app):
    logging.info("Starting up the bot")
    await setup_redis()
    storage = RedisStorage(redis_client.get_redis())
    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)
    dp.include_router(add_paper_router)
    dp.include_router(handle_text_router)
    dp.include_router(send_title_router)
    dp.include_router(view_papers_router)
    dp.include_router(delete_paper_router)
    dp.include_router(help_router)
    dp.include_router(back_to_main_router)
    dp.include_router(select_paper_router)

    app['dp'] = dp

    await bot.set_webhook(config.WEBHOOK_URL)
    logging.info(f"Webhook установлен на {config.WEBHOOK_URL}")

async def on_shutdown(app):
    dp = app['dp']
    logging.info("Удаление webhook")
    await bot.delete_webhook()
    await shutdown_redis()
    await dp.storage.close()

    await bot.session.close()

async def handle(request):
    logging.info("Handling request")
    dp = request.app['dp']
    if request.path == config.WEBHOOK_PATH:
        data = await request.json()
        update = Update(**data)
        logging.info(f"Update received: {update}")
        try:
            await dp.feed_update(bot, update)
            return web.Response(status=200)
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest: {e}")
            return web.Response(status=400)
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            return web.Response(status=500)
    return web.Response(status=404)

def main():
    logging.info("Starting main application")
    app = web.Application()
    app.router.add_post(config.WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host=config.WEBHOOK_HOST, port=config.WEBHOOK_PORT)

if __name__ == '__main__':
    main()

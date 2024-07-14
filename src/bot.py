import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import web
from config import config
from handlers.commands import router as commands_router
from database import setup_redis, shutdown_redis, redis_client
from aiogram.client.bot import DefaultBotProperties

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN_BOT, default=DefaultBotProperties(parse_mode='HTML'))


async def on_startup(app):
    await setup_redis()
    storage = RedisStorage(redis_client._redis)
    dp = Dispatcher(storage=storage)

    dp.include_router(commands_router)
    app['dp'] = dp

    await bot.set_webhook(config.WEBHOOK_URL)
    logging.info(f"Webhook set to {config.WEBHOOK_URL}")


async def on_shutdown(app):
    dp = app['dp']
    logging.info("Removing webhook")
    await bot.delete_webhook()
    await shutdown_redis()
    await dp.storage.close()

    await bot.session.close()


async def handle(request):
    dp = request.app['dp']
    if request.path == config.WEBHOOK_PATH:
        update = await request.json()
        Bot.set_current(bot)
        Dispatcher.set_current(dp)
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    return web.Response(status=404)


def main():
    app = web.Application()
    app.router.add_post(config.WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host=config.WEBHOOK_HOST, port=config.WEBHOOK_PORT)


if __name__ == '__main__':
    main()

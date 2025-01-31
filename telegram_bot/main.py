from config import *

import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.handlers.payment import yookassa_wrapper
from bot.main_handler import router as subrouter
from bot.middlewares import UserMiddleware, RevizorMiddleware
from bot.filters import ChatTypeFilter

main_router = Router()

main_router.message.outer_middleware.register(UserMiddleware())
main_router.callback_query.outer_middleware.register(UserMiddleware())
main_router.callback_query.outer_middleware.register(CallbackAnswerMiddleware())

main_router.message.filter(ChatTypeFilter())
main_router.callback_query.filter(ChatTypeFilter())

main_router.message.middleware.register(RevizorMiddleware())
main_router.callback_query.middleware.register(RevizorMiddleware())

main_router.include_router(subrouter)

@main_router.startup()
async def webhook_setup(bot: Bot) -> None:
    await bot.set_webhook(f"{BOT_WEBHOOK_URL}{BOT_WEBHOOK_PATH}", secret_token=TELEGRAM_SECRET)


def main() -> None:
    dp = Dispatcher()
    dp.include_router(main_router)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app = web.Application()

    app.router.add_post(YOOKASSA_WEBHOOK_PATH, yookassa_wrapper(bot))

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=TELEGRAM_SECRET
    )

    webhook_requests_handler.register(app, path=BOT_WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=BOT_SERVER_HOST, port=BOT_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()

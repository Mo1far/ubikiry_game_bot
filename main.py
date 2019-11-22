from aiogram import Dispatcher

from bot.core import executor

from bot import handlers, db, callback_query


def start():
    executor.start_polling()


if __name__ == '__main__':
    while True:
        try:
            start()
        except:
            pass

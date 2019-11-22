from aiogram.dispatcher.filters.state import StatesGroup, State


class EthereumAddress(StatesGroup):
    get_address = State()
    check_transaction = State()
    change_address = State()

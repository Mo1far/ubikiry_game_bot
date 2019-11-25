from aiogram.types import KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton

check_transaction_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Check', callback_data='check_address'))
check_transaction_kb.add(InlineKeyboardButton('Change the wallet address', callback_data='change_address'))

main_kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb_start.row(KeyboardButton('Help'))

main_kb_approve = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb_approve.row(KeyboardButton('Help'), KeyboardButton('About me'))

clan_statistic = InlineKeyboardButton('Clan statistic', callback_data='clan_statistic')

change_address = InlineKeyboardButton('Change the wallet address', callback_data='change_address')


def get_about_menu(is_clan_leader=False):
    if is_clan_leader:
        kb = InlineKeyboardMarkup().add(clan_statistic).add(change_address)
        return kb
    else:
        kb = InlineKeyboardMarkup().add(change_address)
        return kb

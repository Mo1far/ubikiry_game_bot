from decimal import Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.core import dp, bot
from bot.db import User, Clan, ClanHistory
from bot.etherscan import get_transaction_value
from bot.texts import texts
import bot.keyboards as kb
import bot.config as config
from bot.States import EthereumAddress


@dp.callback_query_handler(lambda x: x.data == 'check_address')
async def check_transaction_status(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    u = User.get_user(user_id)
    transaction_value = await get_transaction_value(u.eth_address)
    if transaction_value >= Decimal(str(config.ENTRY_COST)):
        await bot.send_message(user_id, texts['eth_address']['approve_processing_success'],
                               reply_markup=kb.main_kb_approve)
        await c.message.delete_reply_markup()
        current_state = await state.get_state()
        User.user_approve(user_id=user_id)
        user = User.get_user(c.from_user.id)
        user.balance = transaction_value
        clan = Clan.get_clan(user.clan.id)
        clan.balance += transaction_value
        user.balance = transaction_value
        user.save()
        clan.save()
        if current_state is None:
            return
        await state.finish()
        await c.message.answer('Ваша реферальная ссылка - {}'.format(User.get_ref_link(c.message.from_user.id)))
    else:
        await bot.send_message(user_id, texts['eth_address']['approve_processing_decline'])
        await bot.send_message(user_id, texts['eth_address']['approve_address'].format(
            config.ENTRY_COST,
            config.TARGET_EPH_ADDRESS
        ),
                               reply_markup=kb.check_transaction_kb)
    await bot.answer_callback_query(c.id)


@dp.callback_query_handler(lambda x: x.data == 'clan_statistic')
async def clan_statistic(c: types.CallbackQuery):
    user = User.get_user(user_id=c.from_user.id)
    clan = Clan.get_clan(clan_id=user.clan.id)
    clan_member_count = Clan.get_member_count(clan_id=clan.id)
    await bot.send_message(user.user_id, texts['clan_statistic'].format(clan.id + 1,
                                                                        clan.color,
                                                                        clan_member_count,
                                                                        clan.balance))
    await bot.send_message(user.user_id, ClanHistory.get_history(clan.id))
    await c.answer()


@dp.callback_query_handler(lambda x: x.data == 'change_address')
async def change_address(c: types.CallbackQuery):
    await EthereumAddress.change_address.set()
    await c.message.answer(texts['eth_address']['request'])
    await c.answer()

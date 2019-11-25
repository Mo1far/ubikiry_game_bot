from decimal import Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.db import User, UserHistory, ClanHistory
from bot.core import dp
from bot.texts import texts
from bot.States import EthereumAddress
from bot.utils import validate_ethereum_address, reward_calculation
import bot.keyboards as kb
import bot.config as config


@dp.message_handler(state='*', commands=['start'])
async def start(msg: types.Message):
    if not User.user_exists(msg.from_user.id):
        User.create_user(msg)
        await msg.answer(texts['start']['new_user'], reply_markup=kb.main_kb_start)
    elif User.user_is_approved(msg.from_user.id):
        await msg.answer('Welcome back', reply_markup=kb.main_kb_approve)
    else:
        await msg.answer(texts['start']['new_user'], reply_markup=kb.main_kb_start)
    if not User.eth_address_exist(user_id=msg.from_user.id):
        await msg.answer(texts['eth_address']['request'])
        await EthereumAddress.get_address.set()


@dp.message_handler(state='*', commands=['get_ref_link'])
async def get_ref_link(msg: types.Message):
    await msg.answer(User.get_ref_link(msg.from_user.id))


@dp.message_handler(state='*', regexp='Help')
async def help_regexp(msg: types.Message):
    await msg.answer(texts['help'])


@dp.message_handler(regexp='About me', state='*')
async def user_statistic(msg: types.Message):
    user = User.get_user(msg.from_user.id)
    if user.clan_leader:
        await msg.answer(texts['user_statistic'].format(
            user.clan.id + 1,
            user.clan.color,
            user.clan_level,
            User.get_user_ref_count(msg.from_user.id),
            user.totem_animal,
            reward_calculation(user.user_id),
            Decimal(str(user.clan.balance)),
            user.eth_address,
            User.get_ref_link(msg.from_user.id)
        ), reply_markup=kb.get_about_menu(True))
        await msg.answer(text=await UserHistory.get_history(msg.from_user.id))
    else:
        await msg.answer(texts['user_statistic'].format(
            User.get_user_ref_count(msg.from_user.id),
            user.clan.id + 1,
            user.clan.color,
            user.clan_level,
            user.totem_animal,
            reward_calculation(user.user_id),
            Decimal(str(user.clan.balance)),
            user.eth_address,
            User.get_ref_link(msg.from_user.id)
        ), reply_markup=kb.get_about_menu())
        await msg.answer(await UserHistory.get_history(msg.from_user.id))


@dp.message_handler(state=EthereumAddress.get_address)
async def address_processing(msg: types.Message, state: FSMContext):
    if validate_ethereum_address(msg.text):
        if User.eth_address_unical(msg.text):
            if User.eth_address_exist(msg.from_user.id):
                User.set_eth_address(msg.from_user.id, msg.text)
            else:
                User.set_eth_address(msg.from_user.id, msg.text)
            await EthereumAddress.check_transaction.set()
            if User.is_clan_leader(msg.from_user.id):
                user = User.get_user(msg.from_user.id)
                clan_id = user.clan.id + 1
                await msg.answer(
                    texts['eth_address']['approve_address_for_admin'].format(clan_id, User.get_ref_link(user.user_id)),
                    reply_markup=kb.main_kb_approve)
                User.user_approve(msg.from_user.id)
                await state.finish()
            else:
                await msg.answer(texts['eth_address']['approve_address'].format(
                    config.ENTRY_COST,
                    config.TARGET_EPH_ADDRESS
                ), reply_markup=kb.check_transaction_kb)
                await state.finish()
        else:
            u = User.get_user(msg.from_user.id)
            if u.eth_address == msg.text:
                User.set_eth_address(u.user_id, msg.text)

                await state.finish()
            else:
                await msg.answer(texts['eth_address']['address_decline'])
    else:
        await msg.answer(texts['eth_address']['address_decline'])


@dp.message_handler(state=EthereumAddress.change_address)
async def change_address(msg: types.Message, state: FSMContext):
    if validate_ethereum_address(msg.text):
        if User.eth_address_unical(msg.text):
            if User.eth_address_exist(msg.from_user.id):
                User.set_eth_address(msg.from_user.id, msg.text)
                await msg.answer(texts['eth_address']['address_change_success'])
                if not User.user_is_approved(msg.from_user.id):
                    await msg.answer(texts['eth_address']['approve_address'].format(
                        config.ENTRY_COST,
                        config.TARGET_EPH_ADDRESS
                    ), reply_markup=kb.check_transaction_kb)
                await state.finish()
            else:
                await msg.answer(texts['eth_address']['address_decline'])
        else:
            await msg.answer(texts['eth_address']['address_decline'])
    else:
        await msg.answer(texts['eth_address']['address_decline'])


@dp.message_handler(commands=['save'])
async def history(msg: types.Message):
    print(config.admin_list, msg.from_user.id)
    if msg.from_user.id in config.admin_list:
        await UserHistory.store_all_user()
        await ClanHistory.store_all_clans()
        await msg.answer('Stored')

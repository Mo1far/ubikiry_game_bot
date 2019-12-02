from typing import Tuple
from decimal import Decimal

from bot import config

from bot.core import bot
from bot.texts import texts


class SecureLink(str):

    @staticmethod
    def encode_link(user_id: int, clan_id: int):
        bot_name = bot.get_me()['name']
        encode_user_id = (user_id + 149) * 3
        encode_clan_id = (clan_id + 149) * 4
        return f'https://telegram.me/ClashofClansonIDLplatformBot?start={encode_user_id}-{encode_clan_id}'

    @staticmethod
    def decode_link(link: str) -> Tuple[int, int]:
        s = link.strip('https://telegram.me/ClashofClansonIDLplatformBot?start=')
        encode_user_id, encode_clan_id = s.split('-')
        decode_user_id = int(encode_user_id) // 3 - 149
        decode_clan_id = int(encode_clan_id) // 4 - 149
        return decode_user_id, decode_clan_id


def validate_ethereum_address(address: str) -> bool:
    if address.startswith('0x') and len(address) == 42:
        return True
    return False


def calculate_tree_reward(user, deel_balance=Decimal(str(0))):
    from bot.db import User
    refferals = User.select().where(User.inviter_id == user.user_id)
    if refferals.count() == 0:
        # print('last rekursion', user.user_id, f'balance = {deel_balance}')
        return Decimal(str(user.balance))
    else:
        # deel_balance += Decimal(str(user.balance))
        for refferall in refferals:
            # print('recursion to', refferall.user_id, f'balance = {deel_balance}')
            deel_balance += calculate_tree_reward(refferall, deel_balance=deel_balance)
            # print('for balance', deel_balance)
        return deel_balance + Decimal(str(user.balance))


def reward_calculation(user_id) -> float:
    from bot.db import User
    user = User.get_user(user_id)
    if user.clan_level < 4:
        # user_discount = config.DISCOUNT_TABLE[user.clan.color][user.clan_level - 1] \
        #                            - config.DISCOUNT_TABLE[user.clan.color][user.clan_level]
        user_discount = config.DISCOUNT_TABLE[user.clan.color][user.clan_level] \
                        - config.DISCOUNT_TABLE[user.clan.color][user.clan_level + 1]
    else:
        user_discount = Decimal('0.0')
    user_ref_count = User.get_user_ref_count(user_id)
    if user.totem_animal == 'Dragon':
        personal_allowance = Decimal('0.15')
    elif user.totem_animal == 'Lion':
        personal_allowance = Decimal('0.10')
    elif user.totem_animal == 'Wolf':
        personal_allowance = Decimal('0.05')

    deal = calculate_tree_reward(user)
    if user.clan_leader:
        reward = (user_discount + personal_allowance) * user.clan.balance
        print('cl_reward', f'({user_discount}+{personal_allowance})*{deal}={reward} {user.first_name}')
    else:
        reward = (user_discount + personal_allowance) * deal
        print('cl_reward', f'({user_discount}+{personal_allowance})*{deal}={reward} {user.first_name}')
    return reward


async def send_round_result(user_id, ref_count, totem_animal, clan_color, reward, clan_balance):
    await bot.send_message(user_id, texts['user_round_result']['round_total'].format(
        ref_count,
        totem_animal,
        clan_color,
        clan_balance,
        reward
    ))


async def send_seagun_result(user_id):
    await bot.send_message(user_id, texts['user_round_result']['seagun_result'])


async def send_clan_member_result(clan, result_balance):
    from bot.db import User
    clan_members = User.select().where(User.clan == clan)
    if clan_members.count() > 0:
        for member in clan_members:
            await bot.send_message(member.user_id, texts['user_round_result']['clan_result'].format(
                result_balance,
                clan.color
            ))


async def send_user_history_result(user):
    date = f'{user.date_ended.day}.{user.date_ended.month}.{user.date_ended.year}  {user.date_ended.hour}:{user.date_ended.minute}'
    await bot.send_message(user.user_id, texts['user_history'].format(date,
                                                                      user.ref_count,
                                                                      user.reward
                                                                      ))


async def send_next_round_date(user, clan_color):
    await bot.send_message(user.user_id, texts['user_round_result']['next_round_date'].format(clan_color,
                                                                                              user.totem_animal))

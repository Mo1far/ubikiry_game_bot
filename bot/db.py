import os
from datetime import datetime
from decimal import Decimal
from bot.texts import texts
from bot.core import bot
from peewee import *
from aiogram import types

from bot.config import clan_leader_list
from bot.utils import SecureLink, reward_calculation, send_round_result, send_seagun_result, send_clan_member_result, \
    send_user_history_result, send_next_round_date

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db


class ClanHistory(BaseModel):
    pass


class Relationship(BaseModel):
    pass


class User(BaseModel):
    pass


class UserHistory(BaseModel):
    pass


class Clan(BaseModel):
    id = IntegerField(unique=True)
    leader = ForeignKeyField(User, backref='clan_leader', null=True)
    color = CharField(default='White')
    balance = DecimalField(default='0.0')

    @classmethod
    def get_clan(cls, clan_id: int):
        return cls.get(id=clan_id)

    @classmethod
    def get_clan_without_leader(cls):
        clan = cls.get(leader=None)
        return clan

    @classmethod
    def create_clan(cls, clan_id: int) -> None:
        cls.create(
            id=clan_id
        )

    @classmethod
    def get_member_count(cls, clan_id: int) -> int:
        clan = cls.get_clan(clan_id=clan_id)
        q = User.select().where(User.clan == clan)
        return q.count()

    @classmethod
    def get_seagun(cls):
        seagun_id = Clan.select().order_by(-cls.balance)[0].leader
        seagun_user = User.get(User.id == seagun_id)
        return seagun_user.user_id

    @classmethod
    def get_clan_for_new_user(cls):
        query = Clan.select().where(Clan.leader).order_by(Clan.balance)
        return query[0]


class User(BaseModel):
    user_id = IntegerField(unique=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    clan_leader = BooleanField(default=False)
    clan = ForeignKeyField(Clan, backref='clan_member')
    clan_level = IntegerField(default=9)
    totem_animal = CharField(default='Wolf')
    eth_address = CharField(null=True)
    is_approved = BooleanField(default=False)
    inviter_id = IntegerField(default=0)
    balance = DecimalField(default='0')
    is_seagun = BooleanField(default=False)

    @classmethod
    def user_approve(cls, user_id: str):
        u = User.get_user(user_id=user_id)
        u.is_approved = True
        u.save()

    @classmethod
    def is_clan_leader(cls, user_id: str) -> bool:
        user = User.get_user(user_id)
        if user.clan_leader:
            return True
        return False

    @classmethod
    def set_eth_address(cls, user_id: int, address: str):
        user = User.get_user(user_id)
        user.eth_address = address
        user.save()

    @classmethod
    def eth_address_exist(cls, user_id: int) -> bool:
        user = User.get_user(user_id)
        if user.eth_address:
            return True
        return False

    @classmethod
    def eth_address_unical(cls, address: str) -> bool:
        query = cls().select().where(cls.eth_address == address)
        return not query.exists()

    @classmethod
    def get_ref_link(cls, user_id: int):
        clan_id = User.get_user(user_id).clan.id
        ref_link = SecureLink.encode_link(user_id, clan_id)
        return ref_link

    @classmethod
    def get_user_ref_count(cls, user_id: int):
        ref_count = User.select().where(cls.inviter_id == user_id,
                                        cls.is_approved).count()
        return ref_count

    @classmethod
    def get_user(cls, user_id):
        return cls.get(user_id=user_id)

    @classmethod
    def increase_ref_count(cls, user_id, referral_id):
        user = cls.get_user(user_id)
        referral = cls.get_user(referral_id)
        Relationship.create_referal(user.id, referral.id)
        user.save()

    @classmethod
    def user_exists(cls, user_id):
        query = cls().select().where(cls.user_id == user_id)
        return query.exists()

    @classmethod
    def user_is_approved(cls, user_id: int) -> bool:
        query = cls().select().where(cls.user_id == user_id, cls.is_approved == True)
        return query.exists()

    @classmethod
    def create_clan_leader(cls, msg: types.Message):
        clan = Clan.get_clan_without_leader()
        user = cls.create(
            user_id=msg.from_user.id,
            user_name=msg.from_user.username,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name,
            clan=clan,
            clan_level=1,
            clan_leader=True
        )
        clan.leader = user
        clan.save()

    @classmethod
    def create_ref_user(cls, msg, invited_id, clan_id):
        clan = Clan.get_clan(clan_id)
        invited_user = User.get_user(invited_id)
        if invited_user.clan_level < 9:
            clan_level = invited_user.clan_level + 1
        else:
            clan_level = 9

        user = cls.create(
            user_id=msg.from_user.id,
            user_name=msg.from_user.username,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name,
            is_admin=False,
            clan=clan,
            clan_level=clan_level,
            inviter_id=invited_id
        )

    @classmethod
    def create_raw_user(cls, msg):
        clan = Clan.get_clan_for_new_user()
        print(clan.id)
        clan_level = 9

        user = cls.create(
            user_id=msg.from_user.id,
            user_name=msg.from_user.username,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name,
            is_admin=False,
            clan=clan,
            clan_level=clan_level,
        )

    @classmethod
    def create_user(cls, msg: types.Message):
        if msg.from_user.id in clan_leader_list:
            cls.create_clan_leader(msg)
        elif msg.get_args():
            invited_id, clan_id = SecureLink.decode_link(msg.text)
            cls.create_ref_user(msg, invited_id, clan_id)
        else:
            cls.create_raw_user(msg)


class UserHistory(BaseModel):
    user_id = IntegerField()
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    totem_animal = CharField(default='Walf')
    date_ended = DateTimeField()
    ref_count = IntegerField(default=0)
    reward = FloatField(default=0)

    @classmethod
    async def store_user(cls, user):
        reward = reward_calculation(user.user_id)
        ref_count = User.get_user_ref_count(user.user_id)
        user_history = cls.create(
            user_id=user.user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            totem_animal=user.totem_animal,
            date_ended=datetime.now(),
            ref_count=ref_count,
            reward=reward
        )
        clan_color = user.clan.color
        await send_round_result(user_history.user_id,
                                ref_count,
                                user_history.totem_animal,
                                clan_color,
                                reward,
                                user.clan.balance
                                )

        if ref_count >= 3:
            user.totem_animal = 'Dragon'
        if ref_count == 2:
            user.totem_animal = 'Lion'
        else:
            user.totem_animal = 'Wolf'
        user.save()
        if user.clan.balance >= 0.04:
            clan_color = 'Black'
        elif user.clan.balance >= 0.02:
            clan_color = 'Red'
        else:
            clan_color = 'White'
        await send_next_round_date(user, clan_color=clan_color)

    @classmethod
    async def clean_all_ref(cls):
        users = User.select()
        for user in users:
            user.inviter_id = 0
            user.balance = Decimal('0.0')
            user.save()

    @classmethod
    async def store_all_user(cls):
        users = User.select()
        for user in users:
            await cls.store_user(user=user)
        await cls.clean_all_ref()

    @classmethod
    async def get_history(cls, user_id: int) -> str:

        query = UserHistory.select().where(UserHistory.user_id == user_id)
        if query.exists():
            for record in query:
                await send_user_history_result(record)
        # return f" Last round - totem - {user.totem_animal} ref_count - {user.ref_count}"


class ClanHistory(BaseModel):
    id = IntegerField()
    color = CharField()
    balance = FloatField()

    @classmethod
    async def store_clan(cls, clan):
        cls.create(
            id=clan.id,
            color=clan.color,
            balance=clan.balance
        )
        if clan.balance >= 10.0:
            clan.color = 'Black'
        elif clan.balance >= 5.0:
            clan.color = 'Red'
        else:
            clan.color = 'White'
        # await send_clan_member_result(clan, balance_result)
        # clan.balance = 0
        clan.save()

    @classmethod
    async def store_all_clans(cls):
        # leader_clan = Clan.select().order_by(-Clan.balance)
        # best_clan_id = leader_clan[0]
        # seagun = best_clan_id.leader
        # print(type(seagun)#
        seagun_user_id = Clan.get_seagun()
        clans = Clan.select()
        for clan in clans:
            await cls.store_clan(clan)
        await send_seagun_result(seagun_user_id)
        await ClanHistory.clean_clan_balance()

    @classmethod
    def get_history(cls, clan_id):
        clan = ClanHistory.get(id=clan_id)
        return f'''Stats of the last round:
Clan color - {clan.color}
Total Clan Fees - {clan.balance}
'''

    @classmethod
    async def clean_clan_balance(cls):
        clans = Clan.select()
        for clan in clans:
            clan.balance = Decimal('0.0')
            clan.save()


if not os.path.exists('users.db'):
    db.create_tables([User, Relationship, Clan, UserHistory, ClanHistory])
    for i in range(48):
        Clan.create_clan(i)
# создаём таблицы, запустить 1 раз и закомментировать
# db.create_tables([User, Relationship, Clan, UserHistory])

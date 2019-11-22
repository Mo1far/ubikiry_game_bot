from decimal import Decimal
import json
import asyncio

import aiohttp
from bot.config import ETHERSCAN_API_KEY, TARGET_EPH_ADDRESS, ENTRY_COST, request_str


async def get_response(address: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(request_str.format(address, ETHERSCAN_API_KEY)) as response:
            return await response.text()


async def get_transaction_value(address: str) -> float:
    r = await get_response(address)
    data = json.loads(r)
    # print(data)
    for operations in data['result']:
        if float(operations['value']) / 1000000000000000000 >= ENTRY_COST and \
                operations['to'].lower() == TARGET_EPH_ADDRESS.lower():
            print('trans=', Decimal(operations['value']) / Decimal(str(1000000000000000000)))
            return Decimal(operations['value']) / Decimal(str(1000000000000000000))
    return Decimal(str(0.0))

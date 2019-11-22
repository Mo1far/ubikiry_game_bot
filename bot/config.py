import os
from decimal import Decimal

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API')
request_str = 'http://api.etherscan.io/api?module=account&action=txlist&\
address={}&startblock=0&endblock=99999999&sort=asc&apikey={}'
TARGET_EPH_ADDRESS = '0x395FC2b949CDcE03a11068A473218E7dBf93C402'
ENTRY_COST = float(os.environ.get('ENTRY_COST'))

admin_list = [213447542, 235619648]

clan_leader_list = [845058706,
                    568618101,
                    743871859,
                    785165178,
                    541460441,
                    856332746,
                    404963270,
                    875584167,
                    937079997,
                    926654520,
                    875017985,
                    702541341,
                    800534312,
                    889242121,
                    676651060,
                    918921613,
                    464243276,
                    729156534,
                    589929333,
                    372840544,
                    488297594,
                    414964972,
                    447696433,
                    836477604,
                    748419526,
                    851631521,
                    826478194,
                    674582836,
                    490018200,
                    266337736,
                    966062930,
                    803350790,
                    611378961,
                    473225229,
                    832074765,
                    612170488,
                    549831818,
                    499847958,
                    858102779,
                    707758913,
                    722731915,
                    634056663,
                    412152095,
                    519379304,
                    343389879,
                    524318035,
                    947773060,
                    ]
REF_LINK_TEMPLATE = 'https://telegram.me/{}?clan={}&ref={}'

SECURE_KEY = b'14914914'

DISCOUNT_TABLE = {
    'Black': {
        1: Decimal(str(0.35)),
        2: Decimal(str(0.25)),
        3: Decimal(str(0.15)),
        4: Decimal(str(0.05)),
        5: Decimal(str(0.05)),
        6: Decimal(str(0.05)),
        7: Decimal(str(0.05)),
        8: Decimal(str(0.05)),
        9: Decimal(str(0.05)),
    },
    'Red': {
        1: Decimal(str(0.25)),
        2: Decimal(str(0.18)),
        3: Decimal(str(0.12)),
        4: Decimal(str(0.05)),
        5: Decimal(str(0.05)),
        6: Decimal(str(0.05)),
        7: Decimal(str(0.05)),
        8: Decimal(str(0.05)),
        9: Decimal(str(0.05)),
    },
    'White': {
        1: Decimal(str(0.15)),
        2: Decimal(str(0.11)),
        3: Decimal(str(0.07)),
        4: Decimal(str(0.05)),
        5: Decimal(str(0.05)),
        6: Decimal(str(0.05)),
        7: Decimal(str(0.05)),
        8: Decimal(str(0.05)),
        9: Decimal(str(0.05)),
    }
}

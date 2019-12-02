texts = {
    'start': {
        'new_user': '''“We invite you join “Clash of Clans”! Below is a list of rules, as well as answers to commonly asked questions.

The goal of the game is to attract as many users as possible into your chain (clan), via the invitation process which occurs through our bot. Only those users who join and make a minimum purchase of LAW coins (0.05 ETH or more) are considered.
The game involves 47 clans. A clan consists of a chain of people inviting each other, with the depth limited to nine levels.
The game takes place in periods - rounds of 7 days. It starts on Monday and ends exactly one week later, the following Monday. On the same day (at the end of the round) the final tally is collected. All settlements take place once a week and are paid in ETH; each clan has its own ETH address.
Each participant, regardless of their status, will be able to receive their own statistics.
''',
        'old_user': '''Welcome back'''
    },
    'eth_address': {
        'request': 'Enter your Ethereum address here to join the game.',
        'address_decline': 'Your ETH address is incorrect or it is already used by another person. Check again and resubmit.',
        'approve_address': 'Send {} ETH to {} and click “Check” in order to count your funds',
        'approve_address_for_admin': 'You are now the head of the clan № {}, congratulations! This is your referral link - {}',
        'approve_processing_decline': 'Maybe you made a mistake or payment has not been made yet. Please verify your status and press “Check” again after 2-3 minutes.',
        'approve_processing_success': 'Your payment was successful, press the button  "About" to get your referral link. By bringing other users to the clan, you can get your Totem animal and increase your rewards!',
        'Error': 'You address wrong',
        'address_change_start': 'Enter you Ethereum address for game.',
        'address_change_success': 'Address changed successfully.'
    },
    'help': '''- Game process
The game process is based on rounds of play, the duration of each round is 1 week. The round starts on Mon at 12-00 Moscow time, and ends on the next Mon at 10-00 Moscow time. The summation of results and payment of rewards is carried out within 24 hours after the completion of the round.
Summing up takes place in our channel: https://t.me/GameCClans.


- Brief rules
Our game is called “Clash of Clans”. The essence of the game is to determine the winning clan for each round. Each week according to the results of the round, we will pay rewards.
Rewards are paid from funds raised by the clan. 
In return for the funds that the user sends to the clan account, he receives LAW coins.  LAW is a native cryptocurrency of IDL (https://idledgers.com/).
To receive LAW, you must register in Ubikiri via Telegram and create a LAW wallet. 
 

Your reward depends on the following parameters - your clan color, your totem animal, and your level.
The color of the clan is assigned depending on how much the clan has collected over the last week:
Black - 10 ETH
Red - 5 ETH
else - White
A totem animal is assigned to you depending on the number of members joining the clan from your referral link. 
Dragon - 15 members
Lion - 10 members
Wolf - 5 members
You can be at the following levels within the clan: 
Level 1 - Head of clan 
Level 2 - Head assistant 
Level 3 - Warlord
Level 4-9 - Ronin
The level depends on the length of the chain of people who invited you to the clan.


The number of clans is limited to the number 47, when the number of clans reaches this number, we will remove the weakest clan at the end of each round, as well as this we will remove any clan that collects less than 0.5 ETH per round. 
The head of the clan that collected the largest amount for the round receives the Shogun title and receives additional rewards. Those additional rewards and the procedure for their collection are announced before the start of each round in our channel https://t.me/GameCClans.

- If you need help or you have questions, please join https://t.me/GameCClans, we will be glad to assist you.
''',
    'user_statistic': '''Clan statistics:
Clan number - {},
Clan color - {},
Your level in Clan - {},
The number of participants invited by you - {},
Totem animal - {},
Reward in the current round - {},
Total Clan Fees - {}.

Your ETH address for reward - {}.

Your referral link - {}.

                         ''',
    'clan_statistic': '''Clan number - Х
Clan color - Х
The number of Clan members - Х
Total Clan Fees - Х
''',
    'user_round_result': {
        "round_total": """Another round is over. 
Here are the stats for the last round:
- The number of participants invited by you (referrals) - 1
- Totem animal - Wolf
- Clan color - White
- Account balance of clan - 0.06
- Your reward - 0.0054 ETH
""",
        'seagun_result': """Your clan won this round and you have become a Shogun, you will soon receive an additional reward.”""",
        'next_round_date': """“According to the results of the last round, the following parameters have been changed for the next round:
- Clan color- {}
- Totem animal- {}.”
"""
    },
    'user_history': """Round stats before {}:
The number of participants invited by you: {}
Your reward: {}
"""
}

start = """
"""

help = "What exactly are you interested in?"

g = """At the beginning of the game, 47 participants were appointed as heads of the clans, we initially invited to these positions people who showed the best performance in the airdrop campaign of our partner project, Cryptotribunal.
Further, once a week, we select the best participant in each clan, the one who personally attracted the most funds to the system - this can be one big deal/transaction or attracting a large number of participants in several transactions, etc. They are then appointed as a new head of their own clan (Taking their chain with them), and are invited to a separate Telegram chat specially created for discussion between the heads of clans.
In addition, the head of the clan will be able to receive statistics on his clans performance.
Among the heads of the clans, the person who collected the most money during the week receives the status of Shogun, as well as an extra payment of 1 ETH.
"""

f = """
When summing up the results, each participant receives a clan and personal percentage value that he will get from the purchases across his chain of participants next week. This figure can even go up to 50%! According to the results of the week, each participant will be distributed by color, totem animal, and level within the clan.
"""

h = """
Color - each clan has its own color, the color is assigned depending on how much the clan has collected over the past week:


Amount in ETH
Black
10
Red
5
White
3

In fact, color gives the percentage earnings that you have while being in the clan:
{таблица}
"""

j = """
Each participant will have a totem animal. On the basis of this, each participant, regardless of level, receives an additional personal discount. This personal discount is determined by the number of people attracted by the participant.
Dragon.
“Dragon” discount is 15%, a participant will get it by attracting 15 people.
Lion (Shishi).
“Lion” discount is 10%, a participant will get it by attracting 10 people.

Wolf (Okami).
“Wolf” discount is 5%, a participant will get it by attracting 5 people.
"""

k = """
The participant is a red wolf at the third level. A new member followed his link and bought LAW for 0.3 ETH, his reward would be:
(( 12%-5%)+5%)*0.3= 0,036 ETH
The participant as a lion at the second level will get:
(( 18%-12%)+10%)*0.3= 0,048 ETH
The reward of the head of the clan (dragon) will be:
(( 25%-18%)+15%)*0,3= 0,063 ETH
"""

q = """
Suppose I’m already in a clan and at some level and invite a referral. Can you describe the chain of events between me and this referral. How would this happen?
He receives a link from you where to send ETH in exchange for LAW. Then he sends ETH, receives a link to register at http://ubikiri.com/, and receives a link to invite the referral further along his chain. Then before the end of the week (1 round of the game) they create a LAW wallet to receive the acquired amount of LAW at the weeks conclusion. At the same time, this purchase automatically falls under you and your clan.

If I raise the most money, how do I become the head of a clan? Do I just displace the previous one?

No. You create a new clan, and your whole chain follows you into it.

When will I find out which clan I got in?

Once you pay ETH and get a link to invite other members.

When will I know at what level (what discount) I have?

Once you pay ETH and get a link to invite other members.

When can I begin to attract people?

Once you pay ETH and get a link to invite other members. 

Can I find out whom I invited?

Yes, this information will be available to you, you will see the list of Telegram nicknames.

Can I move to another clan?

No, but you can collect the most money among your clan participants, become a clan head and automatically create your new clan.
"""

import argparse
from distutils.util import strtobool

from lcu_driver import Connector
from score_calculator import Calculator
from utils import wait_for_task

# TODO rewrite as a class this with Willump

connector = Connector()
calc = Calculator()
display_name = ''
summoner_id = ''
gameflow_phase = 'None'
queue_desc = ''
my_role = ''
sylas_ban = False
any_role = False
sylas_score = 0
their_team = {}
sylas_roles = {'middle', 'top', 'jungle'}
draft_modes = {'Draft Pick', 'Ranked Solo/Duo', 'Ranked Flex'}

@connector.ready
async def connect(connection):
    global display_name
    global summoner_id
    print("connected to LCU API")
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    while summoner.status != 200:
        print('log in...', end='\r')
        summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    else:
        summoner_json = await summoner.json()
        summoner_id = summoner_json['summonerId']
        display_name = summoner_json['displayName']
        print(f"hello {display_name} ({summoner_id})")

@connector.close
async def disconnect(_):
    print("disconnected from LCU API")
    await connector.stop()

# listen for champs
@connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def session_update(connection, event):
    global my_role
    global sylas_ban
    global sylas_score
    global their_team
    if gameflow_phase == 'ChampSelect': # and queue_desc in {'Draft Pick', 'Ranked Solo/Duo', 'Ranked Flex'}:
        if 517 in event.data['bans']['myTeamBans'] or 517 in event.data['bans']['theirTeamBans']:
            if not sylas_ban:
                print('Sylas is banned...')
                sylas_ban = True
        elif event.data['timer']['phase'] == 'FINALIZATION':
            # after all picks are locked check incremental calc matches batch calc
            try:
                batch_calc = calc.team_strength(their_team)
                assert sylas_score == batch_calc, f'incremental calc {sylas_score} should equal batch calc {batch_calc}'
            except AssertionError as e:
                print(e)
        else:
            if not my_role:
                # get what role we were assigned
                for player in event.data['myTeam']:
                    if player['cellId'] == event.data['localPlayerCellId']:
                        my_role = player['assignedPosition']
            if my_role in sylas_roles or any_role:
                for player in event.data['theirTeam']:
                    if player['championId']:
                        champ_name = calc.int_to_name[player['championId']]
                        if champ_name not in their_team:
                            their_team[champ_name] = calc.champs_tiers[champ_name] if champ_name in calc.champs_tiers else 'bad'
                            sylas_score += calc.champ_strength(champ_name)
                            if len(their_team)==1:
                                print(f'{their_team}\nsylas score: {sylas_score}')
                            else:
                                print(f'\033[A\033[A{their_team}\nsylas score: {sylas_score}') #\033[A is ANSI escape character for return to start of previous line

# listen for queue description
@connector.ws.register('/lol-gameflow/v1/session', event_types=('UPDATE',))
async def session_update(connection, event):
    global queue_desc
    queue_desc = event.data['gameData']['queue']['description']

# listen for champ select / not champ select
@connector.ws.register('/lol-gameflow/v1/gameflow-phase', event_types=('UPDATE',))
async def session_update(connection, event):
    global gameflow_phase
    global my_role
    global sylas_ban
    global sylas_score
    global their_team
    if queue_desc in {'Draft Pick', 'Ranked Solo/Duo', 'Ranked Flex'}:
        if gameflow_phase != 'ChampSelect' == event.data:
            print('---------------enter-champ-select-session---------------')
        if gameflow_phase == 'ChampSelect' != event.data:
            print('---------------leave-champ-select-session---------------')
            # reset some stuff
            my_role = ''
            sylas_ban = False
            sylas_score = 0
            their_team = {}
    gameflow_phase = event.data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--late", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help='enable this flag if starting the app while already in Champ Select')
    parser.add_argument("--any-role", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help='enable this flag if you want to to get results regardless of your role')
    args = parser.parse_args()
    if args.late: gameflow_phase = "ChampSelect"
    if args.any_role: any_role = True

    wait_for_task('LeagueClientUx.exe')
    connector.start()

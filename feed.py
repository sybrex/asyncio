import asyncio
import time
import argparse
import random
import json


STATES = [
    'Dangerous Attack', 'Attack', 'In Possession', 'Corner', 'Goal Kick', 'Penalty', 'Direct Free Kick',
    'Simple Free Kick', 'Throw In', 'Goal', 'Yellow Card', 'Red Card', 'Substitution', 'Injury',
    'Zoned Free Kick', 'Zoned Throw', 'Offside', 'Corner', 'Dangerous Free Kick', 'Free Kick'
]
TEAMS = [
    'Liverpool', 'Manchester City', 'Leicester', 'Chelsea', 'Manchester Utd', 'Wolves', 'Sheffield Utd',
    'Tottenham', 'Arsenal', 'Burnley', 'Crystal Palace', 'Everton', 'Newcastle', 'Southampton', 'Brighton',
    'West Ham', 'Watford', 'Bournemouth', 'Aston Villa', 'Norwich'
]
MARKETS = [
    {'code': 'MRFT', 'name': 'Match Result Full Time', 'bets': {'1': 1.3, 'X': 2.3, '2': 1.7}}
]
# Match duration 90 min
DURATION = 5400
# Delay between updates 1-5 sec
DELAY = 5
# Only one connection is allowed
CLIENT = {'reader': None, 'writer': None}


class Football:
    def __init__(self, id):
        self.id = id
        self.home_team = random.choice(TEAMS)
        self.away_team = random.choice(TEAMS)
        self.time = random.randint(0, DURATION)
        self.state = random.choice(STATES)
        self.markets = MARKETS
        self.generated = time.time()

    def __str__(self):
        return json.dumps({
            'generated': self.generated,
            'id': self.id,
            'home_team': self.home_team,
            'away_team': self.away_team,
            'time': self.time,
            'state': self.state,
            'markets': self.markets
        })

    def random_update(self, seconds):
        self.state = random.choice(STATES)
        self.time = self.time + seconds
        if self.time > DURATION:
            self.time = 1
        self.generated = time.time()
        for index, market in enumerate(self.markets):
            for bet, odds in market['bets'].items():
                if random.choice([True, False]):
                    delta = (random.random() - 0.5) / 10
                    new_odds = round(odds + delta, 2)
                    self.markets[index]['bets'][bet] = new_odds if new_odds > 1 else odds


async def run_game(game):
    while True:
        delay = random.randint(1, DELAY)
        await asyncio.sleep(delay)
        game.random_update(delay)
        print(f'Game #{game.id} time {game.time} sec. updated {game.generated}')
        if CLIENT['writer']:
            try:
                message = f'{game}\n'
                CLIENT['writer'].write(message.encode())
                await CLIENT['writer'].drain()
            except (BrokenPipeError, ConnectionResetError):
                CLIENT['reader'] = None
                CLIENT['writer'] = None


def handle_client(reader, writer):
    CLIENT['reader'] = reader
    CLIENT['writer'] = writer
    print(f'Client connected {CLIENT}')


async def run_server(host, port, games_count):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    for id in range(games_count):
        game = Football(id)
        print(f'Game #{game.id} {game.home_team} - {game.away_team} Time: {game.time} sec')
        asyncio.create_task(run_game(game))

    async with server:
        await server.serve_forever()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1', help='Host')
    parser.add_argument('--port', type=int, default=5000, help='Port')
    parser.add_argument('--count', type=int, default=5, help='Number of games')
    args = parser.parse_args()
    asyncio.run(run_server(args.host, args.port, args.count))


if __name__ == '__main__':
    main()

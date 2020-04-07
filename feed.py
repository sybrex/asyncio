import asyncio
import socket
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
DELAY = 3


class FootballEvent:
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

    def update(self, seconds):
        self.state = random.choice(STATES)
        self.time = self.time + seconds
        self.generated = time.time()
        for index, market in enumerate(self.markets):
            for bet, odds in market['bets'].items():
                if random.choice([True, False]):
                    delta = (random.random() - 0.5) / 10
                    new_odds = round(odds + delta, 2)
                    self.markets[index]['bets'][bet] = new_odds if new_odds > 1 else odds


async def run_event(loop, client, event):
    print(f'{event.home_team} - {event.away_team} Time: {event.time} sec')
    time.sleep(0.1)
    for msg in range(100):
        delay = random.randint(1, DELAY)
        await asyncio.sleep(delay)
        event.update(delay)
        await loop.sock_sendall(client, str(event).encode('utf8'))


async def handle_client(loop, client, events_count):
    tasks = []
    for i in range(1, events_count+1):
        event = FootballEvent(i)
        tasks.append(asyncio.create_task(run_event(loop, client, event)))
    await asyncio.gather(*tasks)


async def run_server(loop, server, events_count):
    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(loop, client, events_count))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1', help='Host')
    parser.add_argument('--port', type=int, default=5000, help='Port')
    parser.add_argument('--count', type=int, default=5, help='Number of events')
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((args.host, args.port))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_server(loop, server, args.count))


if __name__ == '__main__':
    main()

import aiohttp
import asyncio
from xml.etree import ElementTree as et

from leaderboard import Leaderboard
from user import User
import utils

API_BASE = "http://steamcommunity.com/stats/457210/leaderboards/"


class SEUM:
    def __init__(self):
        self.leaderboards = []  # A list of all our leaderboard objects
        self.users = {}  # A dict containing all our users
        self.il_ranks = []  # A list ordered based on user's points
        self.speedrun_ranks = []  # A list ordered based on user's points
        self.blacklist = [
            76561198164767409,
            76561198207329533,
            76561198091891577,
            76561198799346514,
            76561198071518285,
            76561198161611895,
            76561198134306075,
            76561198124820368,
            76561198071518285,
            76561198253149751,
            76561198084036142,
            76561198032264503
        ]  # A blacklist of steam id's we don't want to count (hackers)
        self.loop = asyncio.get_event_loop()
        self.ready = False

    def get_user(self, steamid):
        return self.users.get(steamid)

    def get_rank(self, key, steamid):
        return getattr(self, "{}_ranks".format(key)).index(self.get_user(steamid)) + 1

    def get_leaderboard(self, leaderboard_id):
        for leaderboard in self.leaderboards:
            if leaderboard.leaderboard_id == leaderboard_id:
                return leaderboard

    def easiest_maps_to_top10(self, amount=5):
        maps_with_less_than_10_entries = [leaderboard for leaderboard in self.leaderboards if leaderboard.total_entries < 10]
        easiest_maps = sorted(
            (
                leaderboard
                for leaderboard in self.leaderboards
                if leaderboard.top_10_standard_deviation > 0
            ),
            key=lambda l: l.top_10_standard_deviation,
            reverse=True
        )[:amount]
        maps = maps_with_less_than_10_entries + easiest_maps
        return maps[:amount]

    async def update_data_task(self):
        while True:
            await self.update_leaderboards()
            self.ready = True
            await asyncio.sleep(300)

    async def get_leaderboard_ids(self):
        url = API_BASE + "?xml=1"

        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                tree = et.fromstring(await response.text())

        for data in tree.iter("leaderboard"):
            ldb = Leaderboard(self, data)
            self.leaderboards.append(ldb)

    async def update_leaderboards(self):
        # Loop through and make the http call required to update the leaderboard data we have
        count = 0
        utils.progress_bar(0, len(self.leaderboards))
        for ldb in self.leaderboards:
            if await ldb.update_data():
                self.update_users_for_leaderboard(ldb)
            count += 1
            utils.progress_bar(count, len(self.leaderboards))

        # Now setup the ranks list; IE simply create a list of users ordered based on the points they have
        self.il_ranks = sorted(self.users.values(), key=lambda x: x.get_data("il", "points"), reverse=True)
        self.speedrun_ranks = sorted(self.users.values(), key=lambda x: x.get_data("speedrun", "points"), reverse=True)

    def update_users_for_leaderboard(self, leaderboard):
        for entry in leaderboard:
            if entry.steamid in self.blacklist:
                continue

            # User does not exist, create and add it to our dict
            if entry.steamid not in self.users:
                user = User(self, entry)
                self.users[entry.steamid] = user
            # User exists
            else:
                self.users.get(entry.steamid).update_entry(entry)

    def update_users(self):
        # Now loop through and do what's required for actual leaderboard data manipulation
        print("Getting all entries for users...")
        count = 0
        utils.progress_bar(0, len(self.leaderboards))
        for ldb in self.leaderboards:
            for entry in ldb:
                if entry.steamid in self.blacklist:
                    continue

                # User does not exist, create and add it to our dict
                if entry.steamid not in self.users:
                    user = User(self, entry)
                    self.users[entry.steamid] = user
                # User exists
                else:
                    self.users.get(entry.steamid).update_entry(entry)

            count += 1
            utils.progress_bar(count, len(self.leaderboards))

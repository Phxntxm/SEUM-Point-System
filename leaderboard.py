"""IMPORTANT NOTE: Leaderboard class uses etree, Entry uses BeautifulSoup.
This is for simplicity's sake of using each object but MAY BE CONFUSING SINCE THEY ARE BOTH XML PARSING CLASSES"""

import utils
import aiohttp
import statistics
from bs4 import BeautifulSoup as bs


class Leaderboard:
    def __init__(self, seum, data):
        # Data is the xml data given from the leaderboards xml page, each entry looks like the following
        """
        <url>
        http://steamcommunity.com/stats/457210/leaderboards/2239322/?xml=1
        </url>
        <lbid>2239322</lbid>
        <name>endless0_v4</name>
        <display_name>Endless Mode</display_name>
        <entries>3519</entries>
        <sortmethod>2</sortmethod>
        <displaytype>1</displaytype>
        """
        self.seum = seum  # A simple attribute in order to access the parent class
        self._leaderboard_data = data
        self._entries = []  # The actual entries as Entry objects
        self.times = {}  # A dict containing times, mapped to a list of entries with this time
        self.top_10_standard_deviation = 0

    def __iter__(self):
        for entry in self._entries:
            yield entry

    def __len__(self):
        return len(self._entries)

    def __str__(self):
        return self.name

    def __getitem__(self, key):
        return self._entries[key]

    async def update_data(self):
        url = utils.API_BASE + "{}/?xml=1".format(self.leaderboard_id)

        try:
            with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soup = bs(await response.text(), "html.parser")
        except:
            return False

        self._entries = []
        for entry in soup.find_all("entry"):
            if int(entry.steamid.text) in self.seum.blacklist:
                continue

            e = Entry(self, entry)
            self._entries.append(e)
            # We have a different dict for times, so that we can handle ties
            time_temp = self.times.get(e.score, [])
            self.times[e.score] = time_temp + [e]
        if len(self._entries) > 2:
            self.top_10_standard_deviation = statistics.variance(sorted(entry.score for entry in self)[:10])

        return True

    def get_rank(self, user):
        for count, entries in enumerate(self.times.values()):
            if user in [e.user for e in entries]:
                return count + 1

    @property
    def speedrun(self):
        return "Speedrun" in self.name

    @property
    def endless(self):
        return self.leaderboard_id == "2239322"

    @property
    def il(self):
        return not self.speedrun and not self.endless

    @property
    def record(self):
        return self.times[sorted(self.times)[0]]

    @property
    def name(self):
        return self._leaderboard_data.find("display_name").text

    @property
    def leaderboard_id(self):
        return int(self._leaderboard_data.find("lbid").text)

    @property
    def total_entries(self):
        return int(self._leaderboard_data.find("entries").text)


class Entry:
    def __init__(self, ldb, data):
        # Data is the xml tag for an actual entry, format looks like the following
        """
        <steamid>76561198174538383</steamid>
        <score>1590239</score>
        <rank>1</rank>
        <ugcid>18446744073709551615</ugcid>
        <details>
        <![CDATA[ ]]>
        </details>
        """
        self._data = data
        self.leaderboard = ldb

    @property
    def steamid(self):
        return int(self._data.steamid.text)

    @property
    def user(self):
        return self.leaderboard.seum.get_user(self.steamid)

    @property
    def rank(self):
        for count, entries in enumerate(self.leaderboard.times.values()):
            if self in entries:
                return count + 1

    @property
    def top_10(self):
        return self.rank <= 10

    @property
    def top_3(self):
        return self.rank <= 3

    @property
    def record(self):
        return self.rank == 1

    @property
    def score(self):
        points = int(self._data.score.text)
        # Endless mode is the only one with a different scoring system
        if self.leaderboard.endless:
            return points
        # Normal modes are measured in milliseconds, so just divide by 1000
        else:
            return points / 1000

    @property
    def points(self):
        return utils.convert_rank_to_points(self.rank)

    @property
    def srpr(self):
        return self.leaderboard.record[0].score / self.score

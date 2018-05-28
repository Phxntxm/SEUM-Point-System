import utils


class User:
    def __init__(self, seum, entry):
        # A user will be instantiated the first time an entry is found, so that's what we're accepting
        self.steamid = entry.steamid
        self.points = 0
        self.seum = seum  # A simple attribute in order to access the parent class
        self.name = None  # The display name saved for a user

        # This dictionary contains the data classes for each type of run
        self._data = {
            "il": Data("il", self),
            "speedrun": Data("speedrun", self)
        }

    def __hash__(self):
        return self.steamid

    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.steamid)

    def __lt__(self, other):
        if not isinstance(other, User):
            raise TypeError("Cannot compare type {} to User".format(type(other)))
        return self.steamid < other.steamid

    def __gt__(self, other):
        if not isinstance(other, User):
            raise TypeError("Cannot compare type {} to User".format(type(other)))
        return self.steamid > other.steamid

    def __ge__(self, other):
        if not isinstance(other, User):
            raise TypeError("Cannot compare type {} to User".format(type(other)))
        return self.steamid >= other.steamid

    def __le__(self, other):
        if not isinstance(other, User):
            raise TypeError("Cannot compare type {} to User".format(type(other)))
        return self.steamid <= other.steamid

    def update_entry(self, entry):
        if entry.leaderboard.il:
            self._data.get("il").update(entry)
        elif entry.leaderboard.speedrun:
            self._data.get("speedrun").update(entry)

    def get_data(self, attribute, key="il"):
        """A dynamic method to call getattr on the Data instance"""
        return getattr(self._data[key.lower()], attribute)

    @property
    def total_runs(self):
        return self._data.get("il").total_runs + self._data.get("speedrun").total_runs

class Data:
    """This class is used to seperate data between IL's and speedruns; key is what denotes which this is"""


    def __init__(self, key, user):
        self.key = key
        self.user = user
        self._entries = {} # This will be mapped from a leaderboard ID, to this user's entry on it
        
        # The initialization of our data points
        self.top_10s = 0
        self.top_3s = 0
        self.records = 0
        self.average_rank = 0
        self.average_srpr = 0
        self.points = 0

    def update(self, entry):
        """Takes an entry and calculates what new data it will contain"""
        old_entry = self._entries.get(entry.leaderboard.leaderboard_id)

        # First check if the new rank is a top 10 rank
        if entry.top_10:
            # We only have to do something if the old rank was NOT a top 10
            if old_entry and old_entry.rank > 10 or old_entry is None:
                self.top_10s += 1
        if entry.top_3:
            if old_entry and old_entry.rank > 3 or old_entry is None:
                self.top_3s += 1
        if entry.record:
            if old_entry and old_entry.rank > 1 or old_entry is None:
                self.records += 1

        # An average is a total of the entries / the length of entries
        # Therefore if we just track the average, we can multiply by the current length of entries
        # Then add to it, and divide by the new length of entries to get our new average
        # For ranks we should round, as there should never be a decimal
        if old_entry:
            # This means that the length hasn't changed, and a rank has
            self.average_rank = round((self.average_rank * len(self._entries) - old_entry.rank + entry.rank) / len(self._entries))
            self.average_srpr = (self.average_srpr * len(self._entries) - old_entry.srpr + entry.srpr) / len(self._entries)
            self.points -= old_entry.points
            self.points += entry.points
        else:
            # This means it's a new entry
            self.average_rank = round((self.average_rank * len(self._entries) + entry.rank) / (len(self._entries) + 1))
            self.average_srpr = (self.average_srpr * len(self._entries) + entry.srpr) / (len(self._entries) + 1)
            self.points += entry.points

        self._entries[entry.leaderboard.leaderboard_id] = entry

    @property
    def rank(self):
        return self.user.seum.get_rank(self.key, self.user.steamid)

    @property
    def worst_ranks(self):
        return sorted((entry for entry in self._entries.values()), key=lambda e: e.rank, reverse=True)

    @property
    def worst_srpr(self):
        return sorted((entry for entry in self._entries.values()), key=lambda e: e.srpr)

    @property
    def total_runs(self):
        return len(self._entries)
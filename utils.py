import sys

API_BASE = "http://steamcommunity.com/stats/457210/leaderboards/"


def progress_bar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


def convert_rank_to_points(rank):
    rank = int(rank)
    # Our cutoff number, anything below this is worth a point, anything above is not
    if rank > 250:
        return 0

    points = 200 - (rank - 1)
    if points < 0:
        points = 1
    else:
        points = points ** 2 / 200
    return max(1, points)

import asyncio
import time

from seum import SEUM

loop = asyncio.get_event_loop()


def run(func):
    loop.run_until_complete(func())

seum = SEUM()
now = time.time()
run(seum.get_leaderboard_ids)
run(seum.update_leaderboards)
total_time = time.time() - now
print("Took {:.2f} seconds".format(total_time))
# seum.update_users()


if __name__ == "__main__":
    now = time.time()
    user = seum.get_user(76561198015678746)

    il_rank           = user.get_data("il", "rank")
    floor_rank        = user.get_data("speedrun", "rank")
    lb_count          = "{} / {}".format(user.total_runs, len(user.seum.leaderboards))

    il_records        = user.get_data("il", "records")
    il_top_10s        = user.get_data("il", "top_10s")
    il_top_3s         = user.get_data("il", "top_3s")
    il_av_rank        = user.get_data("il", "average_rank")
    il_av_srpr        = user.get_data("il", "average_srpr") * 100
    il_worst_ranks    = user.get_data("il", "worst_ranks")[:5]
    il_worst_ranks    = "\n".join(["{entry.leaderboard.name} ({entry.rank})".format(entry=entry) for entry in il_worst_ranks])
    il_worst_srpr     = user.get_data("il", "worst_srpr")[:5]
    il_worst_srpr     = "\n".join(["{entry.leaderboard.name} ({srpr:.2f})".format(entry=entry, srpr=entry.srpr * 100) for entry in il_worst_srpr])


    floor_records     = user.get_data("speedrun", "records")
    floor_top_10s     = user.get_data("speedrun", "top_10s")
    floor_top_3s      = user.get_data("speedrun", "top_3s")
    floor_av_rank     = user.get_data("speedrun", "average_rank")
    floor_av_srpr     = user.get_data("speedrun", "average_srpr") * 100
    floor_worst_ranks = user.get_data("speedrun", "worst_ranks")[:5]
    floor_worst_ranks = "\n".join(["{entry.leaderboard.name} ({entry.rank})".format(entry=entry) for entry in floor_worst_ranks])
    floor_worst_srpr  = user.get_data("speedrun", "worst_srpr")[:5]
    floor_worst_srpr  = "\n".join(["{entry.leaderboard.name} ({srpr:.2f})".format(entry=entry, srpr=entry.srpr * 100) for entry in floor_worst_srpr])


    print("""
Data for {user} (IL Rank {il_rank}, Floor Rank {floor_rank})
Leaderboard count: {lb_count}
IL Data:
---------------------------------------
Records: {il_records}
Top 10's: {il_top_10s}
Top 3's: {il_top_3s}
Average rank: {il_av_rank:.2f}
Average SRPR: {il_av_srpr:.2f}%
Worst Ranks:
---------------------------------------
{il_worst_ranks}
---------------------------------------
Worst SPRR:
---------------------------------------
{il_worst_srpr}
---------------------------------------

Floor Data:
---------------------------------------
Records: {floor_records}
Top 10's: {floor_top_10s}
Top 3's: {floor_top_3s}
Average rank: {floor_av_rank:.2f}
Average SRPR: {floor_av_srpr:.2f}%
Worst Ranks:
---------------------------------------
{floor_worst_ranks}
---------------------------------------
Worst SPRR:
---------------------------------------
{floor_worst_srpr}
---------------------------------------
""".format(
    user=user,
    il_rank=il_rank,
    floor_rank=floor_rank,
    lb_count=lb_count,
    il_records=il_records,
    il_top_10s=il_top_10s,
    il_top_3s=il_top_3s,
    il_av_rank=il_av_rank,
    il_av_srpr=il_av_srpr,
    il_worst_ranks=il_worst_ranks,
    il_worst_srpr=il_worst_srpr,
    floor_records=floor_records,
    floor_top_10s=floor_top_10s,
    floor_top_3s=floor_top_3s,
    floor_av_rank=floor_av_rank,
    floor_av_srpr=floor_av_srpr,
    floor_worst_ranks=floor_worst_ranks,
    floor_worst_srpr=floor_worst_srpr
))
    total_time = time.time() - now
    print("Took {:.2f} seconds".format(total_time))


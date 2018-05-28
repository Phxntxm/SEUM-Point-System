from discord.ext import commands

class Commands:

    def __init__(self, bot):
        self.bot = bot

    @property
    def seum(self):
        return self.bot.seum

    @commands.command()
    async def data(self, ctx, steamid: int):
        user = self.seum.get_user(steamid)

        il_rank = user.get_data("il", "rank")
        floor_rank = user.get_data("speedrun", "rank")
        lb_count = "{} / {}".format(user.total_runs, len(user.seum.leaderboards))

        il_records = user.get_data("records")
        il_top_10s = user.get_data("top_10s")
        il_top_3s = user.get_data("top_3s")
        il_av_rank = user.get_data("average_rank")
        il_av_srpr = user.get_data("average_srpr") * 100
        il_worst_ranks = user.get_data("worst_ranks")[:5]
        il_worst_ranks = "\n".join(
            ["{entry.leaderboard.name} ({entry.rank})".format(entry=entry) for entry in il_worst_ranks])
        il_worst_srpr = user.get_data("il", "worst_srpr")[:5]
        il_worst_srpr = "\n".join(
            ["{entry.leaderboard.name} ({srpr:.2f})".format(entry=entry, srpr=entry.srpr * 100) for entry in
             il_worst_srpr])

        data = f"""
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
"""
        await ctx.send(f"```\n{data}```")

def setup(bot):
    bot.add_cog(Commands(bot))
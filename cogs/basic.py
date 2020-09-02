import discord
from discord.ext import commands


class Basic(commands.Cog):
    """
    매우 기본적인 명령어들이 있는 Cog 입니다.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="핑", aliases=["ping", "vld", "ㅔㅑㅜㅎ"])
    async def ping(self, ctx: commands.Context):
        """
        매우 기본적인 핑 명령어입니다.
        """
        await ctx.send(f":ping_pong: 퐁! ({round(self.bot.latency * 1000)}ms)")


def setup(bot: commands.Bot):
    bot.add_cog(Basic(bot))

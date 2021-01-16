import discord
import asyncio
from discord.ext import commands
import aiohttp
import main


class Git(commands.Cog):
    """
    Git 관련 기능들이 있는 Cog 입니다.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await main.is_whitelisted(ctx)

    @commands.command(name="reload_file")
    async def check_craft(self, ctx: commands.Context, *, arg):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://raw.githubusercontent.com/eunwoo1104/KCP/master/' + arg) as response:
                if response.status == 200 or response.status == 304:
                    data = await response.text(encoding="UTF-8")
                    with open(arg, "w", encoding="UTF-8") as f:
                        f.write(data)
                    await ctx.send(f"O, CODE {response.status} LEN {len(data)}")
                else:
                    await ctx.send(f"X, CODE {response.status}")


def setup(bot: commands.Bot):
    bot.add_cog(Git(bot))

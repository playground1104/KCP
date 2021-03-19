import json
import discord
import asyncio
from discord.ext import commands
import aiohttp
import os


def get_bot_settings() -> dict:
    """
    봇 설정 파일을 파이썬 dict로 리턴합니다.
    """
    with open('bot_settings.json', 'r', encoding="UTF-8") as f:
        return json.load(f)


async def is_whitelisted(ctx):
    """
    Cog 관련 명령어를 봇 소유자나 화이트리스트에 등록된 유저만 사용하게 만드는 코드입니다.
    """
    return ctx.author.id in get_bot_settings()["whitelist"]


class Git(commands.Cog):
    """
    Git 관련 기능들이 있는 Cog 입니다.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await is_whitelisted(ctx)

    @commands.command(name="reload_file")
    async def reload_file(self, ctx: commands.Context, *, arg):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://raw.githubusercontent.com/eunwoo1104/KCP/master/' + arg) as response:
                if response.status == 200 or response.status == 304:
                    data = await response.text(encoding="UTF-8")
                    with open(arg, "w", encoding="UTF-8") as f:
                        f.write(data)
                    await ctx.send(f"O, CODE {response.status} LEN {len(data)}")
                else:
                    await ctx.send(f"X, CODE {response.status}")
    
    @commands.command(name="make_dir")
    async def make_dir(self, ctx: commands.Context, *, arg):
        if not os.path.exists(directory):
            os.makedirs(directory)
            await ctx.send(f"O")
        else:
            await ctx.send(f"X, EXISTS")

def setup(bot: commands.Bot):
    bot.add_cog(Git(bot))

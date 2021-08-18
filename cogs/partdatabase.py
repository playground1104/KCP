import json
import csv
import os

from discord.ext import commands


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


class PartDB(commands.Cog):
    """
    무장 확인 관련 기능들이 있는 Cog 입니다.
    """

    async def cog_check(self, ctx):
        return await is_whitelisted(ctx)

    seasondict = {}

    @commands.command(name="seasondict_reload")
    async def reloadcmd(self, ctx):
        self.reload()

    def reload(self):
        for x in list(self.seasondict.keys())[:]:
            self.unload(x)
        for x in os.listdir("partdb"):
            if x.endswith('.csv'):
                self.load('partdb/' + x, os.path.split(x)[-1].replace('.csv', ''))

    @commands.command(name="seasondict_printlist")
    async def printlist(self, ctx):
        await ctx.send('\n'.join(self.seasondict.keys()))

    def load(self, file: str, name: str):
        with open(file, 'r', encoding='UTF-8') as f:
            partdb = {}
            for r in csv.reader(f):
                partdb[r[0]] = {'armorthickness': int(r[1]), 'point': float(r[2]), 'tweakoption': str(r[3])}
        self.seasondict[name] = partdb

    def unload(self, name: str):
        del self.seasondict[name]

    def lst(self, season: str) -> dict:
        try:
            return self.seasondict[season]
        except KeyError:
            return {}

    @staticmethod
    def slst(bot: commands.Bot, season: [str, None]) -> dict:
        if season is None:
            return bot.get_cog("PartDB").seasondict[get_bot_settings()["default_season"]]
        try:
            return bot.get_cog("PartDB").seasondict[season]
        except KeyError:
            return bot.get_cog("PartDB").seasondict[get_bot_settings()["default_season"]]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reload()


def setup(bot: commands.Bot):
    bot.add_cog(PartDB(bot))

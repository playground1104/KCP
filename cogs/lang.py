import json
import os

from discord.ext import commands


def get_bot_settings() -> dict:
    """
    봇 설정 파일을 파이썬 dict로 리턴합니다.
    """
    with open('bot_settings.json', 'r', encoding="UTF-8") as f:
        return json.load(f)


class Lang(commands.Cog):
    """
    언어 설정 관련 기능들이 있는 Cog 입니다.
    """

    translationdict = {}

    def load(self, file: str, name: str):
        with open(file, 'r', encoding='UTF-8') as f:
            self.translationdict[name] = json.load(f)

    def unload(self, name: str):
        del self.translationdict[name]

    def fmt(self, lang: str, key: str) -> str:
        try:
            return self.translationdict[lang][key]
        except KeyError:
            return key

    @staticmethod
    def sfmt(bot: commands.Bot, lang: str, key: str) -> str:
        try:
            return bot.get_cog("Lang").translationdict[lang][key]
        except KeyError:
            return key

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        for x in os.listdir("lang"):
            if x.endswith('.json'):
                self.load('lang/'+x, os.path.split(x)[-1].replace('.json', ''))


def setup(bot: commands.Bot):
    bot.add_cog(Lang(bot))

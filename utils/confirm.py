import discord
import asyncio
from discord.ext import commands


async def confirm(bot: commands.Bot, ctx: commands.Context, msg: discord.Message, time: int = 30):
    """
    해당 액션을 할지 확인하는 코루틴 함수입니다.
    :param ctx: 명령어 컨택스트
    :param bot: 디스코드 봇
    :param msg: 메시지
    :param time: 타임아웃 시간 (기본: 30초)
    :return: 승인했을 때는 `True`를, 거절했을 때는 `False`를, 타임아웃때는 `None`을 반환합니다.
    """
    emoji_list = ["⭕", "❌"]

    await msg.add_reaction("⭕")
    await msg.add_reaction("❌")

    def check(reaction, user):
        return str(reaction.emoji) in emoji_list and user == ctx.author

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=time, check=check)
        if str(reaction.emoji) == emoji_list[0]:
            return True
        elif str(reaction.emoji) == emoji_list[1]:
            return False
    except asyncio.TimeoutError:
        return None

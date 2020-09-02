"""
discord.py 봇 탬플릿 by eunwoo1104 (Discord: eunwoo1104#9600)
MIT 라이센스를 지키는 한 자유롭게 이용이 가능합니다.
이 템플릿으로 봇을 제작하기 전에 타입 힌트와 클래스와 비동기 정도는 알고 시작하는 것을 추천합니다.
봇을 제작할 때는 디코파이 문서를 참고하세요.
discord.py 문서: https://discordpy.readthedocs.io/en/latest/index.html
번역중인 문서: https://discordpy.cpbu.xyz/index.html
코드에 문제가 있을 경우 자유롭게 Issue나 Pull Request를 넣어주세요.
"""
import asyncio
import discord
import json
import os
import logging
import websockets
from discord.ext import commands

loop = asyncio.get_event_loop()


def get_bot_settings() -> dict:
    """
    봇 설정 파일을 파이썬 dict로 리턴합니다.
    """
    with open('bot_settings.json', 'r', encoding="UTF-8") as f:
        return json.load(f)


logger = logging.getLogger('discord')
logging.basicConfig(level=logging.INFO)  # DEBUG/INFO/WARNING/ERROR/CRITICAL
handler = logging.FileHandler(filename=f'{get_bot_settings()["bot_name"]}.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = "stable_token"

if get_bot_settings()["debug"]:
    """
    만약에 봇 설정 파일에 debug 항목이 true로 되있다면 stable_token이 아닌 canary_token이 불러와집니다.
    이를 원하지 않는다면 debug를 false로 해주세요.
    """
    token = "canary_token"
    print("Bot running in debug mode.")


async def get_prefix(bot, message):
    """
    프리픽스를 리턴해주는 코루틴입니다.
    """
    return commands.when_mentioned_or(*[get_bot_settings()["default_prefix"]])(bot, message)


bot = commands.Bot(command_prefix=get_prefix, help_command=None)


async def is_whitelisted(ctx):
    """
    Cog 관련 명령어를 봇 소유자나 화이트리스트에 등록된 유저만 사용하게 만드는 코드입니다.
    """
    return ctx.author.id in get_bot_settings()["whitelist"]


async def change_presence():
    """
    봇의 상태메시지를 계속 변경해주는 코드입니다.
    바뀌는 시간은 sleep_time 변수 변경으로 가능합니다.
    추천되는 설정은 15초입니다.
    """
    sleep_time = 15
    await bot.wait_for("ready")
    while True:
        if len(get_bot_settings()["presence"]) == 1:
            await bot.change_presence(activity=discord.Game(get_bot_settings()["presence"][0]))
            await asyncio.sleep(sleep_time)
            continue
        for x in get_bot_settings()["presence"]:
            try:
                await bot.change_presence(activity=discord.Game(x))
                await asyncio.sleep(sleep_time)
            except (asyncio.streams.IncompleteReadError, discord.ConnectionClosed, websockets.exceptions.ConnectionClosedError):
                logger.warning(f"Failed changing presence. Skipping this string: {x}")
                await asyncio.sleep(sleep_time)
            except Exception as ex:
                logger.error(f"Unexpected error occurred during changing presence: {ex.__str__()}")
                await asyncio.sleep(sleep_time)


@bot.event
async def on_ready():
    """
    봇이 실행될 때 작동하는 코드입니다.
    **주의!**: 이 코드는 한번만 실행되는 것이 아니라, 연결이 끊어진 이후에 다시 실행될 수 있습니다.
    (출처: discord.py 문서 https://discordpy.cpbu.xyz/api.html#discord.on_ready)
    """
    logger.info("Bot online.")


@bot.command(name="cog", aliases=["cogs", "코그"])
@commands.check(is_whitelisted)
async def _cog_panel(ctx):
    """
    Cog를 로드하거나 언로드할 수 있는 명령어입니다.
    이모지 반응으로 컨트룔이 가능합니다.
    """
    load = "⏺"
    unload = "⏏"
    reload = "🔄"
    up = "⬆"
    down = "⬇"
    stop = "⏹"
    emoji_list = [load, unload, reload, up, down, stop]
    msg = await ctx.send("잠시만 기다려주세요...")
    for x in emoji_list:
        await msg.add_reaction(x)
    cog_list = [c.replace(".py", "") for c in os.listdir("./cogs") if c.endswith(".py")]
    cogs_dict = {}
    base_embed = discord.Embed(title=f"{get_bot_settings()['bot_name']} Cog 관리 패널", description=f"`cogs` 폴더의 Cog 개수: {len(cog_list)}개", color=discord.Color.from_rgb(225, 225, 225))
    for x in cog_list:
        if x in [x.lower() for x in bot.cogs.keys()]:
            cogs_dict[x] = True
        else:
            cogs_dict[x] = False
    cogs_keys = [x for x in cogs_dict.keys()]
    selected = cogs_keys[0]
    selected_num = 0

    def check(reaction, user):
        return user == ctx.author and str(reaction) in emoji_list

    while True:
        tgt_embed = base_embed.copy()
        for k, v in cogs_dict.items():
            if k == selected:
                k = "▶" + k
            tgt_embed.add_field(name=k, value=f"상태: {'로드됨' if v else '언로드됨'}", inline=False)
        await msg.edit(content=None, embed=tgt_embed)
        try:
            reaction, user = await bot.wait_for("reaction_add", check=check, timeout=60)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            await msg.edit(content="Cog 관리 패널이 닫혔습니다.", embed=None)
            break
        if str(reaction) == down:
            if selected_num+1 == len(cogs_keys):
                wd = await ctx.send("이미 마지막 Cog 입니다.")
                await wd.delete(delay=3)
            else:
                selected_num += 1
                selected = cogs_keys[selected_num]
        elif str(reaction) == up:
            if selected_num == 0:
                wd = await ctx.send("이미 첫번째 Cog 입니다.")
                await wd.delete(delay=3)
            else:
                selected_num -= 1
                selected = cogs_keys[selected_num]
        elif str(reaction) == reload:
            if not cogs_dict[selected]:
                wd = await ctx.send("먼저 Cog를 로드해주세요.")
                await wd.delete(delay=3)
            else:
                bot.reload_extension("cogs." + selected)
        elif str(reaction) == unload:
            if not cogs_dict[selected]:
                wd = await ctx.send("이미 Cog가 언로드되있습니다.")
                await wd.delete(delay=3)
            else:
                bot.unload_extension("cogs." + selected)
                cogs_dict[selected] = False
        elif str(reaction) == load:
            if cogs_dict[selected]:
                wd = await ctx.send("이미 Cog가 로드되있습니다.")
                await wd.delete(delay=3)
            else:
                bot.load_extension("cogs." + selected)
                cogs_dict[selected] = True
        elif str(reaction) == stop:
            await msg.clear_reactions()
            await msg.edit(content="Cog 관리 패널이 닫혔습니다.", embed=None)
            break
        await msg.remove_reaction(reaction, ctx.author)


# Cog를 불러오는 스크립트
[bot.load_extension(f"cogs.{x.replace('.py', '')}") for x in os.listdir("./cogs") if x.endswith('.py')]

# 봇 상태 메시지를 변경하는 코드 준비
loop.create_task(change_presence())

# 봇 실행
bot.run(get_bot_settings()[token])

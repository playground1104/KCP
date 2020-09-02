import discord
from discord.ext import commands
from utils import kspconfig


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

    @commands.command(name="검수")
    async def check_craft(self, ctx: commands.Context):
        msg = ctx.message
        if len(ctx.message.attachments) == 0 or not ctx.message.attachments[0].filename.endswith(".craft"):
            msg = await self.bot.wait_for("message", timeout=30, check=lambda m: m.author.id == ctx.author.id and len(m.attachments) != 0)
        craft = msg.attachments[0]
        craft_content = (await craft.read()).decode("UTF-8")

        blacklist = ["bahaECMJammer", "AMRAAM.EMP", "BD1x1slopeArmor", "BD2x1slopeArmor", "BD1x1panelArmor",
                     "BD2x1panelArmor", "BD3x1panelArmor", "BD4x1panelArmor"]
        armpoint = {"bahaBrowningAnm2": 0.5, "bahaAim9": 1.0, "bahaAim120": 1.5, "bahaChaffPod": 0.5, "bahaCmPod": 0.5,
                    "bahaGau-8": 2, "bahaHiddenVulcan": 1.0}

        armor2 = ["bahaAim9"]

        ap = 0.0

        c = kspconfig.loadl(craft_content.split('\n'))

        part_list = []

        for d in c["PART"]:
            e = '_'.join(d["part"].split("_")[:-1])
            part_list.append(e)
            if e in blacklist:
                return await ctx.send(f"블랙리스트 감지됨-취소\n읽은 파츠 리스트: ```{', '.join(part_list)}```")
            f = armpoint.get(e)
            if f is not None:
                ap += f
            g = 0
            for h in d["MODULE"]:
                if h["name"] == "HitpointTracker":
                    g = int(h["Armor"])
            i = 10
            if e in armor2:
                i = 2
            if g > i:
                return await ctx.send(f"아머 감지됨-취소\n읽은 파츠 리스트: ```{', '.join(part_list)}```")
        if ap <= 15.1:
            return await ctx.send(f"문제가 없습니다.\n읽은 파츠 리스트: ```{', '.join(part_list)}```")
        else:
            return await ctx.send(f"무장 포인트를 초과했습니다.\n읽은 파츠 리스트: ```{', '.join(part_list)}```")


def setup(bot: commands.Bot):
    bot.add_cog(Basic(bot))

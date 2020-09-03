import discord
import asyncio
from discord.ext import commands
from kspconfig import kspconfig


class Basic(commands.Cog):
    """
    매우 기본적인 명령어들이 있는 Cog 입니다.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.channel.id == 681058514797461647 or isinstance(ctx.message.channel, discord.DMChannel)

    @commands.command(name="검수")
    async def check_craft(self, ctx: commands.Context):
        msg = ctx.message
        if len(ctx.message.attachments) == 0 or not ctx.message.attachments[0].filename.endswith(".craft"):
            try:
                await ctx.send("30초 안에 기체 파일을 보내주세요.")
                msg = await self.bot.wait_for("message", timeout=30, check=lambda m: m.author.id == ctx.author.id and len(m.attachments) != 0)
                if not msg.attachments[0].filename.endswith(".craft"):
                    return await ctx.send("`.craft` 파일만 올려야 합니다. 다시 명령어를 실행해주세요.")
            except asyncio.TimeoutError:
                return await ctx.send("시간 만료, 다시 명령어를 실행해주세요.")
        craft = [x for x in msg.attachments if x.filename.endswith(".craft")][0]
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
                return await ctx.send(f"블랙리스트 감지됨-취소\n해당 파츠: `{e}`")
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
                return await ctx.send(f"아머 두께 번경 감지됨-취소")
        if ap <= 15.1:
            return await ctx.send(f"문제가 없습니다.\n파츠 카운트: {len(part_list)}개")
        else:
            return await ctx.send(f"무장 포인트를 초과했습니다. ({ap}점)\n파츠 카운트: {len(part_list)}개")

    @commands.command(name="check")
    async def check_craft_en(self, ctx: commands.Context):
        msg = ctx.message
        if len(ctx.message.attachments) == 0 or not ctx.message.attachments[0].filename.endswith(".craft"):
            try:
                await ctx.send("Please send your craft file in 30 second.")
                msg = await self.bot.wait_for("message", timeout=30, check=lambda m: m.author.id == ctx.author.id and len(m.attachments) != 0)
                if not msg.attachments[0].filename.endswith(".craft"):
                    return await ctx.send("Only `.craft` file is allowed. Please run this command again.")
            except asyncio.TimeoutError:
                return await ctx.send("Timeout, please run this command again.")
        craft = [x for x in msg.attachments if x.filename.endswith(".craft")][0]
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
                return await ctx.send(f"Blacklist Detected-Cancelled\nBlacklisted Part: `{e}`")
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
                return await ctx.send(f"Armor Thickness is changed-Check Cancelled.")
        if ap <= 15.1:
            return await ctx.send(f"No problems.\nPart count: {len(part_list)}")
        else:
            return await ctx.send(f"Exceeded maximum arm point. ({ap} point)\nPart count: {len(part_list)}")


def setup(bot: commands.Bot):
    bot.add_cog(Basic(bot))

import discord
import asyncio
from discord.ext import commands
from kspconfig import kspconfig
import csv


class Basic(commands.Cog):
    """
    매우 기본적인 명령어들이 있는 Cog 입니다.
    """

    partdb = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open('db.csv') as f:
            for r in csv.reader(f):
                self.partdb[r[0]] = {'armorthickness': int(r[1]), 'point': float(r[2]), 'tweakoption': str(r[3])}

    async def cog_check(self, ctx):
        return ctx.message.channel.id == 681058514797461647 or isinstance(ctx.message.channel, discord.DMChannel)

    @commands.command(name="검수")
    async def check_craft(self, ctx: commands.Context):
        msg = ctx.message
        if len(ctx.message.attachments) == 0 or not ctx.message.attachments[0].filename.endswith(".craft"):
            try:
                await ctx.send("30초 안에 기체 파일을 보내주세요.")
                msg = await self.bot.wait_for("message", timeout=30,
                                              check=lambda m: m.author.id == ctx.author.id and len(m.attachments) != 0)
                if not msg.attachments[0].filename.endswith(".craft"):
                    return await ctx.send("`.craft` 파일만 올려야 합니다. 다시 명령어를 실행해주세요.")
            except asyncio.TimeoutError:
                return await ctx.send("시간 만료, 다시 명령어를 실행해주세요.")
        craft = [x for x in msg.attachments if x.filename.endswith(".craft")][0]
        craft_content = (await craft.read()).decode("UTF-8")

        ap = 0.0

        c = kspconfig.loadl(craft_content.split('\n'))

        part_list = []

        error_blacklist = set()
        error_armorthickness = dict()
        error_tweak = dict()

        for d in c["PART"]:
            e = '_'.join(d["part"].split("_")[:-1])
            part_list.append(e)
            try:
                f = self.partdb[e]
            except KeyError:
                error_blacklist.add(e)
                continue
            ap += f['point']
            g = 0
            try:
                m = d["MODULE"]
            except KeyError:
                m = []
            for h in m:
                if h["name"] == "HitpointTracker":
                    g = int(h["Armor"])
                elif h["name"] == "TweakScale":
                    topt = f['tweakoption']
                    cs = float(h["currentScale"])
                    ds = float(h["defaultScale"])
                    if cs > ds and not ("u" in topt):
                        error_tweak[e] = [cs, "u"]
                    elif cs < ds and not ("d" in topt):
                        error_tweak[e] = [cs, "d"]

            t = f['armorthickness']
            if g > t:
                error_armorthickness[e] = [g, t]


        size_split = c["size"].split(',')
        size_width = float(size_split[0])
        size_height = float(size_split[1])
        size_length = float(size_split[2])
        berror_size = (size_width > 19.0005) or (size_height > 8.0005) or (size_length > 20.0005)
        berror_ap = ap > 17.1
        berror_blacklist = False
        berror_armorthickness = False
        berror_tweak = False
        berror_partcount = len(part_list) > 250
        embed = discord.Embed(title="KCP 기체 검수 시스템")
        embed.set_footer(text="오류 제보: Penta#1155")
        if berror_partcount:
            embed.add_field(name="부품 수 초과", value=f"{len(part_list)} > 250")
        else:
            embed.add_field(name="부품 수 정상", value=f"{len(part_list)}부품")

        if len(error_blacklist) > 0:
            embed.add_field(name="금지 부품 사용됨", value=', '.join(error_blacklist))
            berror_blacklist = True
        else:
            embed.add_field(name="금지 부품 미사용", value=f"{len(part_list)}부품")
        if len(error_armorthickness) > 0:
            s = ""
            for k, v in error_blacklist:
                if len(s) != 0:
                    s = s + ", "
                s = s + k + ": " + str(v[0]) + " > " + str(v[1])
            embed.add_field(name="장갑 두께 변경됨", value=s)
            berror_armorthickness = True
        else:
            embed.add_field(name="장갑 두께 정상", value=f"{len(part_list)}부품")

        if len(error_tweak) > 0:
            s = ""
            for k, v in error_tweak:
                if len(s) != 0:
                    s = s + ", "
                s = s + k + ": " + str(v[0])
                if v[1] == "u":
                    s = s + " UT"
                elif v[1] == "d":
                    s = s + " DT"
            embed.add_field(name="트윅스케일 위반", value=s)
            berror_tweak = True
        else:
            embed.add_field(name="트윅스케일 정상", value=f"{len(part_list)}부품")

        if berror_ap:
            embed.add_field(name="무장 점수 초과", value=f"{ap:.1f}점")
        else:
            embed.add_field(name="무장 점수 정상", value=f"{ap:.1f}점")

        if berror_size:
            embed.add_field(name="크기 초과", value=f"약 {size_width:.2f} x {size_height:.2f} x {size_length:.2f}m")
        else:
            embed.add_field(name="크기 정상", value=f"약 {size_width:.2f} x {size_height:.2f} x {size_length:.2f}m")

        if not (berror_ap or berror_armorthickness or berror_blacklist or berror_size or berror_tweak or berror_partcount):
            embed.add_field(name="문제가 없습니다", value=f"{len(part_list)}부품", inline=False)
            embed.colour = 0x00ff00
        else:
            embed.colour = 0xff0000
        return await ctx.send(embed=embed)

    """
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
    """


def setup(bot: commands.Bot):
    bot.add_cog(Basic(bot))

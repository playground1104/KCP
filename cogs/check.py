import discord
import asyncio
from discord.ext import commands
from kspconfig import kspconfig

from cogs import lang, partdatabase


class Check(commands.Cog):
    """
    매우 기본적인 명령어들이 있는 Cog 입니다.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.channel.id == 707591545863536680 or isinstance(ctx.message.channel, discord.DMChannel)

    async def check_craft(self, ctx: commands.Context, langs: str, partdb: dict):
        msg = ctx.message
        if len(ctx.message.attachments) == 0 or not ctx.message.attachments[0].filename.endswith(".craft"):
            try:
                await ctx.send(lang.Lang.sfmt(self.bot, langs, "basic_sendin30").format())
                msg = await self.bot.wait_for("message", timeout=30,
                                              check=lambda m: m.author.id == ctx.author.id and (
                                                          len(m.attachments) != 0))
                if msg.content == "!검수":
                    return
                if not msg.attachments[0].filename.endswith(".craft"):
                    return await ctx.send(lang.Lang.sfmt(self.bot, langs, "basic_onlycraft").format())
            except asyncio.TimeoutError:
                return await ctx.send(lang.Lang.sfmt(self.bot, langs, "basic_timeout").format())
        craft = [x for x in msg.attachments if x.filename.endswith(".craft")][0]
        craft_content = (await craft.read()).decode("UTF-8")

        ap = 0

        c = kspconfig.loadl(craft_content.split('\n'))

        part_list = []

        error_blacklist = set()
        error_armorthickness = dict()
        error_tweak = dict()

        for d in c["PART"]:
            e = '_'.join(d["part"].split("_")[:-1])
            part_list.append(e)
            try:
                f = partdb[e]
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
        berror_ap = ap > 34
        berror_blacklist = False
        berror_armorthickness = False
        berror_tweak = False
        berror_partcount = len(part_list) > 250
        embed = discord.Embed(title=lang.Lang.sfmt(self.bot, langs, "basic_embed_title").format(), description=c["ship"])
        embed.set_footer(text=lang.Lang.sfmt(self.bot, langs, "basic_embed_footer").format())
        if berror_partcount:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_partcount_F_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_partcount_F_value").format(len(part_list)))
        else:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_partcount_P_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_partcount_P_value").format(len(part_list)))

        if len(error_blacklist) > 0:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_partban_F_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_partban_F_value").format(', '.join(error_blacklist)))
            berror_blacklist = True
        else:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_partban_P_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_partban_P_value").format())

        if len(error_armorthickness) > 0:
            s = ""
            for k, v in error_blacklist:
                if len(s) != 0:
                    s = s + ", "
                s = s + k + ": " + str(v[0]) + " > " + str(v[1])
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_armorthickness_F_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_armorthickness_F_value").format(s))
            berror_armorthickness = True
        else:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_armorthickness_P_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_armorthickness_P_value").format())

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
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_tweakscale_F_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_tweakscale_F_value").format(s))
            berror_tweak = True
        else:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_tweakscale_P_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_tweakscale_P_value").format())

        if berror_ap:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_ap_F_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_ap_F_value").format(ap))
        else:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_ap_P_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_ap_P_value").format(ap))

        if berror_size:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_size_F_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_size_F_value").format(size_width, size_height,
                                                                                     size_length))
        else:
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_size_P_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_size_P_value").format(size_width, size_height,
                                                                                     size_length))

        if not (
                berror_ap or berror_armorthickness or berror_blacklist or berror_size or berror_tweak or berror_partcount):
            embed.add_field(name=lang.Lang.sfmt(self.bot, langs, "basic_embed_P_name").format(),
                            value=lang.Lang.sfmt(self.bot, langs, "basic_embed_P_value").format(len(part_list)), inline=False)
            embed.colour = 0x00ff00
        else:
            embed.colour = 0xff0000
        return await ctx.send(embed=embed)

    @commands.command(name="검수")
    async def check_craft_ko_KR(self, ctx: commands.Context):
        await self.check_craft(ctx, "ko_KR", partdatabase.PartDB.slst(self.bot, None))

    @commands.command(name="check")
    async def check_craft_en_US(self, ctx: commands.Context):
        await self.check_craft(ctx, "en_US", partdatabase.PartDB.slst(self.bot, None))

    @commands.command(name="뭉치검수")
    async def check_multi_craft(self, ctx: commands.Context):
        msg = ctx.message
        ans = "```부품 수, 금지부품, 장갑두께, 트윅스케일, 무장점수, 크기"
        craftlist = [x for x in msg.attachments if x.filename.endswith(".craft")]
        await ctx.send("30초 안에 기체 파일들을 보내주세요.")
        while True:
            try:
                msg = await self.bot.wait_for("message", timeout=30,
                                              check=lambda m: m.author.id == ctx.author.id and (
                                                      (len(m.attachments) != 0) or (m.content == "!뭉치검수끝")))
                for x in msg.attachments:
                    if x.filename.endswith(".craft"):
                        craftlist.append(x)
                if msg.content == "!뭉치검수끝":
                    break
            except asyncio.TimeoutError:
                break
        for craft in craftlist:
            craft_content = (await craft.read()).decode("UTF-8")

            ap = 0

            c = kspconfig.loadl(craft_content.split('\n'))

            part_list = []

            error_blacklist = set()
            error_armorthickness = dict()
            error_tweak = dict()

            for d in c["PART"]:
                e = '_'.join(d["part"].split("_")[:-1])
                part_list.append(e)
                try:
                    f = partdatabase.PartDB.slst(self.bot, None)
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
            berror_ap = ap > 34
            berror_blacklist = False
            berror_armorthickness = False
            berror_tweak = False
            berror_partcount = len(part_list) > 250
            ans += f"\n{c['ship']:20}"
            if berror_partcount:
                ans += f"🔴"
            else:
                ans += f"🟢"

            if len(error_blacklist) > 0:
                ans += f"🔴"
                berror_blacklist = True
            else:
                ans += f"🟢"
            if len(error_armorthickness) > 0:
                s = ""
                for k, v in error_blacklist:
                    if len(s) != 0:
                        s = s + ", "
                    s = s + k + ": " + str(v[0]) + " > " + str(v[1])
                ans += f"🔴"
                berror_armorthickness = True
            else:
                ans += f"🟢"

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
                ans += f"🔴"
                berror_tweak = True
            else:
                ans += f"🟢"

            if berror_ap:
                ans += f"🔴"
            else:
                ans += f"🟢"

            if berror_size:
                ans += f"🔴"
            else:
                ans += f"🟢"

            if not (
                    berror_ap or berror_armorthickness or berror_blacklist or berror_size or berror_tweak or berror_partcount):
                ans += f" 🟢"
            else:
                ans += f" 🔴"
        return await ctx.send(ans + "```")


def setup(bot: commands.Bot):
    bot.add_cog(Check(bot))

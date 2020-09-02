import discord
from discord.ext import commands


class Help(commands.Cog):
    """
    도움말 명령어 Cog 입니다.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="도움", aliases=["도움말", "help"])
    async def help(self, ctx: commands.Context):
        base_embed = discord.Embed(title="명령어 리스트", description=f"프리픽스: `{ctx.prefix}`", color=discord.Color.from_rgb(225, 225, 225))
        cogs = [(x, y.get_commands()) for x, y in self.bot.cogs.items()]
        for x in cogs:
            if not bool(x[1]):
                continue
            base_embed.add_field(name=x[0], value='`' + '`, `'.join([c.name for c in x[1]]) + '`',
                                 inline=False)
        await ctx.send(embed=base_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))

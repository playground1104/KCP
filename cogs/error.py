import discord
import json
import logging
from discord.ext import commands


class Error(commands.Cog):
    """
    봇 명령어를 실행할 때 오류가 발생한 경우 오류 정보를 출력하게 만드는 Cog 입니다.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        with open("bot_settings.json", "r", encoding="UTF-8") as f:
            bot_settings = json.load(f)
        logger = logging.getLogger("discord")
        logger.error(error)
        if bot_settings["debug"] is True:
            # 봇 설정 파일에서 디버그 모드가 true로 되어있으면 이 코드를 실행합니다.
            await ctx.send("디버그 모드가 켜져있습니다.")
            raise error
        embed = discord.Embed(title="오류 발생!", description="명령어를 실행하던 도중 오류가 발생했습니다.\nAn error occured while running this command.", colour=discord.Color.red())
        if isinstance(error, commands.BotMissingPermissions):
            embed.add_field(name="BotMissingPermissions", value=f"봇이 필요한 권한을 가지고 있지 않습니다.\nBot is missing required permission(s)."
                                                                f"필요한 권한 | Required Perms: `{', '.join(error.missing_perms)}`")
        elif isinstance(error, commands.CommandNotFound):
            return # await ctx.message.add_reaction(emoji="🤔")
        elif isinstance(error, commands.MissingPermissions):
            embed.add_field(name="MissingPermissions", value="Aㅓ... 합필이면... 잘 알아두세요. 당신은 이 명령어를 실행할 권한이 읎어요.\nWell, you are not allowed to run this comand.\n"
                                                             f"필요한 권한 | You requires: `{', '.join(error.missing_perms)}`")
        elif isinstance(error, commands.CheckFailure):
            embed.add_field(name="CheckFailure", value="`검수` 명령어는 DM으로만 사용 가능합니다.\nYou can run 'check' command only by DM.")
        elif isinstance(error, commands.CommandOnCooldown):
            embed.add_field(name="CommandOnCooldown", value=f'쿨다운이 아직 남았습니다.\nYou are on cooldown.\n({error.retry_after:.2f}secs)')
        elif isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name="MissingRequiredArgument", value=f"누락된 필수 항목이 있습니다.\nMissing required args.\n(`{error.param.name}`)")
        else:
            embed.add_field(name="예기치 않은 오류 발생 | Unexpected Error", value=f"```py\n{error}```")
        await ctx.message.add_reaction("⚠")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Error(bot))

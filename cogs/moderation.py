import discord
from discord.ext import commands
from discord.ext.commands import Context


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def nick(
        self, context: Context, user: discord.User, *, nickname: str = None
    ) -> None:
        """
        Change the nickname of a user on a server.

        :param context: The command context.
        :param user: The user whose nick should be changed
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                description=(
                    "An error occurred while trying to change the nickname of the user."
                    "Make sure my role is above the role of the user you want to change the nickname."
                ),
                color=0xE02B2B,
            )
            await context.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Moderation(bot))

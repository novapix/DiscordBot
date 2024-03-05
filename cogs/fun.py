from discord.ext import commands
from discord.ext.commands import Context

from helpers.extra_functions import get_jokes


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="getjoke",
        description="Gets a Random Joke",
    )
    async def random_joke(self, context: Context):
        """
        Replies with a Random Joke.

        :param context: The Command Context
        """
        success, mes = await get_jokes()
        if success:
            mes = f"Here is a Joke for you: \n{mes}"

        await context.send(content=mes)


def setup(bot) -> None:
    bot.add_cog(Fun(bot))
